from tkinter import ttk
from tkinter import SOLID, NW

from app.windows.shelter.healer.healer_frame import ShelterHealerFrame
from app.windows.shelter.gather.gather_frame import ShelterGatherFrame

from app.windows.shelter.radar.radar_frame import ShelterRadarFrame
from app.windows.shelter.daily.daily_frame import ShelterDailyFrame
from app.windows.shelter.hunt.hunt_frame import ShelterHuntFrame
from app.windows.shelter.water.water_frame import ShelterWaterFrame
from app.windows.shelter.rally.rally_frame import ShelterRallyFrame
from app.windows.shelter.rally.autorally_frame import ShelterAutoRallyFrame
from app.windows.shelter.transfer.transfer_frame import ShelterTransferFrame
from app.windows.shelter.zombi.zombi_frame import ShelterZombiFrame
from app.service.locale_service import Localization


from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager

class SheltersMainFrame(ttk.Frame):
    def __init__(self, parent):
        self.frame: ttk.Frame = super().__init__(parent, padding=(3,3), border=2, borderwidth=3, relief=SOLID)
        self.app = parent
        self.task_manager: TaskManager = self.app.task_manager
        self.user_config: ConfigManager = self.app.user_config
        self.clicker_manager: ClickerManager = self.app.clicker_manager
        self.windows_manager = self.app.windows_manager
        self.game_objects = self.app.game_objects
        self.locale: Localization = self.app.locale
        self.put_shelters_frame()


    def put_shelters_frame(self):
        # self.shelter_healer_frame = ShelterHealerFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )
        self.shelter_gather_frame = ShelterGatherFrame(
            self,
            config=self.user_config,
            task_manager=self.task_manager,
            clicker_manager=self.clicker_manager,
            windows_manager=self.windows_manager,
            game_objects=self.game_objects,
            locale=self.locale
            )
        # self.shelter_gather_autorally_frame = ShelterGatherAutoRallyFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects
        #     )
        # self.shelter_gather_hunt_frame = ShelterGatherHuntFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects
        #     )
        self.shelter_radar_frame = ShelterRadarFrame(
            self,
            config=self.user_config,
            task_manager=self.task_manager,
            clicker_manager=self.clicker_manager,
            windows_manager=self.windows_manager,
            game_objects=self.game_objects,
            locale=self.locale
            )
        # self.shelter_daily_frame = ShelterDailyFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )

        # self.shelter_hunt_frame = ShelterHuntFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects
        #     )
        # self.shelter_water_frame = ShelterWaterFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )
        # self.shelter_rally_frame = ShelterRallyFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )
        # self.shelter_autorally_frame = ShelterAutoRallyFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )
        # self.shelter_transfer_frame = ShelterTransferFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )
        # self.shelter_zombi_frame = ShelterZombiFrame(
        #     self,
        #     config=self.user_config,
        #     task_manager=self.task_manager,
        #     clicker_manager=self.clicker_manager,
        #     windows_manager=self.windows_manager,
        #     game_objects=self.game_objects,
        #     locale=self.locale
        #     )



        self.shelter_gather_frame.grid(row=0, column=0, sticky=NW)
        # self.shelter_gather_autorally_frame.grid(row=0, column=1, sticky=NW)
        # self.shelter_gather_hunt_frame.grid(row=0, column=2, sticky=NW)
        # self.shelter_transfer_frame.grid(row=0, column=3, sticky=NW)

        # self.shelter_healer_frame.grid(row=1, column=0, sticky=NW)
        self.shelter_radar_frame.grid(row=1, column=1, sticky=NW)
        # self.shelter_daily_frame.grid(row=1, column=2, sticky=NW)

        # self.shelter_hunt_frame.grid(row=2, column=0, sticky=NW)
        # self.shelter_water_frame.grid(row=2, column=1, sticky=NW)

        # self.shelter_rally_frame.grid(row=3, column=0, sticky=NW)
        # self.shelter_autorally_frame.grid(row=3, column=1, sticky=NW)
        # self.shelter_zombi_frame.grid(row=3,column=2, sticky=NW)
