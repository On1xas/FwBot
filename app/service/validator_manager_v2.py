import requests
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from tkinter import messagebox
from pydantic import BaseModel
from enum import IntEnum
import logging

from app.service.task_manager import TaskManager
from app.logging import logger
from app.config.config_manager import ConfigManager
from app.service.locale_service import Localization

class StatusCode(IntEnum):
    SUCCESS = 0
    USER_NOT_FOUND = 1001
    DEVICE_NOT_REGISTERED = 1002
    INVALID_LICENSE_KEY = 1003
    LICENSE_EXPIRED = 1004
    TIME_SYNC_ERROR = 1005
    DATABASE_ERROR = 5000
    NETWORK_ERROR = 5001

class LicenseResponse(BaseModel):
    code: StatusCode
    message: str
    exp_time: Optional[datetime] = None
    server_time: Optional[datetime] = None

class ValidatorManager:
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    TIME_SYNC_THRESHOLD = timedelta(seconds=4*3600)

    def __init__(self, app, config: ConfigManager, task_manager: TaskManager):
        self.app = app
        self.locale: Localization = app.locale
        self.config: ConfigManager = config
        self.task_manager = task_manager
        self.server_url = "http://45.144.64.228:5000"
        self._reset_state()

    def _reset_state(self):
        self.server_status = False
        self.online = False
        self.last_connection = None
        self.failed_sync_time = 0

    @property
    def hw_id(self) -> str:
        return str(uuid.getnode())

    def _build_payload(self) -> Dict[str, Any]:
        return {
            "client_id": self.config.user.client_id,
            "token": self.config.user.token,
            "hwID": self.hw_id
        }

    def auth(self) -> LicenseResponse:
        logger.info('Starting authentication process')
        url = f"{self.server_url}/api/v1/auth"

        try:
            response = requests.post(url, json=self._build_payload(), timeout=10)
            return self._process_auth_response(response)

        except requests.exceptions.RequestException as e:
            logger.error(f'Network error: {str(e)}')
            return self._handle_network_error(e)

        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return self._build_error_response(
                StatusCode.DATABASE_ERROR,
                "Internal system error"
            )

    def _process_auth_response(self, response: requests.Response) -> LicenseResponse:
        try:
            response_data = response.json()
            validated = LicenseResponse(**response_data)
        except Exception as e:
            logger.error(f'Invalid response format: {str(e)}')
            return self._build_error_response(
                StatusCode.DATABASE_ERROR,
                "Invalid server response"
            )

        if validated.code == StatusCode.SUCCESS:
            self._update_client_state(validated)
            if not self._check_time_sync(validated.server_time):
                return self._build_error_response(
                    StatusCode.TIME_SYNC_ERROR,
                    "Device time out of sync"
                )
            return validated

        return self._handle_error_cases(validated)

    def _update_client_state(self, response: LicenseResponse):
        self.server_status = True
        self.online = True
        self.last_connection = datetime.now(timezone.utc)

        if response.exp_time:
            self.config.update_exp_time(response.exp_time)

        self.app.user_frame.update_server_status()

    def _check_time_sync(self, server_time: datetime) -> bool:
        local_time = datetime.now(timezone.utc)
        time_diff = abs((local_time - server_time).total_seconds())

        if time_diff > self.TIME_SYNC_THRESHOLD.total_seconds():
            logger.warning(f'Time sync mismatch: {time_diff} seconds')
            return False
        return True

    def _handle_error_cases(self, response: LicenseResponse) -> LicenseResponse:
        error_handlers = {
            StatusCode.USER_NOT_FOUND: self._handle_user_not_found,
            StatusCode.DEVICE_NOT_REGISTERED: self._handle_device_error,
            StatusCode.INVALID_LICENSE_KEY: self._handle_license_error,
            StatusCode.LICENSE_EXPIRED: self._handle_license_expired,
        }

        handler = error_handlers.get(response.code, self._handle_unknown_error)
        return handler(response)

    def _handle_network_error(self, error: Exception) -> LicenseResponse:
        self._reset_state()
        self.app.user_frame.update_server_status()

        if isinstance(error, requests.exceptions.Timeout):
            msg = "Connection timeout"
            code = StatusCode.NETWORK_ERROR
        else:
            msg = "Network connection error"
            code = StatusCode.NETWORK_ERROR

        return self._build_error_response(code, msg)

    def _handle_user_not_found(self, response: LicenseResponse) -> LicenseResponse:
        logger.warning("User not found in system")
        if self.config.first_time_setup:
            return response
        return self._build_error_response(response.code, response.message)

    def _handle_device_error(self, response: LicenseResponse) -> LicenseResponse:
        logger.warning("Device registration required")
        # Add device confirmation logic here
        return response

    def _handle_license_error(self, response: LicenseResponse) -> LicenseResponse:
        logger.warning("Invalid license key")
        self.config.reset_license()
        return response

    def _handle_license_expired(self, response: LicenseResponse) -> LicenseResponse:
        logger.warning("License expired")
        self.config.license_expired = True
        self._stop_application()
        return response

    def _handle_unknown_error(self, response: LicenseResponse) -> LicenseResponse:
        logger.error(f"Unknown error: {response.message}")
        return self._build_error_response(
            StatusCode.DATABASE_ERROR,
            "Unknown server error"
        )

    def _build_error_response(
        self,
        code: StatusCode,
        message: str,
        **kwargs
    ) -> LicenseResponse:
        self._reset_state()
        self.app.user_frame.update_server_status()
        return LicenseResponse(code=code, message=message, **kwargs)

    def _stop_application(self):
        self.task_manager.stop_event.set()
        self.app.validate = False
        self.app.render(self.app.render_license_frame)
        messagebox.showerror(
            "License Error",
            "License has expired. Please contact administrator"
        )

    def check_license_expiration(self):
        if not self.config.user.expired_time:
            return

        exp_time = datetime.strptime(
            self.config.user.expired_time,
            self.DATE_FORMAT
        ).replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > exp_time:
            self._stop_application()
            logger.warning("License expiration detected")

    def sync_with_server_time(self):
        try:
            response = requests.get(
                f"{self.server_url}/api/v1/get_time",
                params={"client_id": self.config.user.client_id},
                timeout=5
            )
            response.raise_for_status()

            data = response.json()
            self.last_connection = datetime.strptime(
                data['time'],
                self.DATE_FORMAT
            ).replace(tzinfo=timezone.utc)

            self.config.update_exp_time(data['exp_time'])
            self.failed_sync_time = 0

        except requests.RequestException as e:
            self.failed_sync_time += 1
            logger.warning(f"Time sync failed ({self.failed_sync_time}/3 attempts)")

            if self.failed_sync_time >= 3:
                self._stop_application()
                messagebox.showerror(
                    "Sync Error",
                    "Critical time sync error. Application stopped"
                )

    def days_until_expiration(self) -> str:
        if not self.config.user.expired_time:
            return self.locale.i10n('day_until_not_active')

        exp_time = datetime.strptime(
            self.config.user.expired_time,
            self.DATE_FORMAT
        ).replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        if exp_time < now:
            return self.locale.i10n('day_until_expired')

        delta = (exp_time - now).days
        return self._format_days(delta, exp_time)

    def _format_days(self, days: int, exp_date: datetime) -> str:
        declension = self.locale.i10n(
            'day_until_day' if days == 1 else
            'day_until_days2' if 2 <= days <= 4 else
            'day_until_days'
        )

        return f"{exp_date.strftime('%d.%m.%Y')} ({days} {declension})"