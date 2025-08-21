import time
import datetime
from pygetwindow import PyGetWindowException
from app.utils.resourse_path import resource_path
from app.utils.cv import find_template_matches, find_template_matches_color, find_template_simple, filter_coordinates
from app.utils.datetime_lib import has_time_passed
from app.service.clicker_manager import ClickerManager
from app.service.window_manager import WindowManager, Window
from app.service.task_manager import TaskManager
from app.service.locale_service import Localization
from app.service.window_manager import Window
from app.logging import logger
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import Label, Entry, Button, SOLID, EW, messagebox, DISABLED, NORMAL
import random

def check_stop_func(method):
    def wrapper(self, *args, **kwargs):
        if not self.task_manager.stop_func:
            logger.info(msg=f"STOP DECORATOR INIT {method.__name__}")
            return method(self, *args, **kwargs)
        else:
            logger.info(msg=f"STOP DECORATOR - STOP PROCESS START - STATUS STOP FUNC TRIGGER [{self.task_manager.stop_func}]")
            return None
    return wrapper


class GameObjectService():
    def __init__(
                self,
                parent,
                windows_manager: WindowManager,
                clicker_manager: ClickerManager,
                task_manager: TaskManager,
                locale: Localization
        ):
        self.app = parent
        self.clicker_manager: ClickerManager = clicker_manager
        self.task_manager: TaskManager = task_manager
        self.locale: Localization = locale
        self.windows_manager: WindowManager = windows_manager
        self.gather_task = {}
        self.gather_stat = {}
        self.gather_object_list = []
        self.radar_task = {}
        self.rally_started = None
        self.rally_task = {}
        self.transfer_task = {}
        self.zombi_task = {}




    @check_stop_func
    def go_to_shelter(self):
        logger.info(msg=f"GAME OBJECT SERVICE: CHECK REGION FUNC")
        path_region_btn = resource_path(relative_path="app\\img\\game_button\\go-region.png")
        path_shelter_btn = resource_path(relative_path="app\\img\\game_button\\go-shelter.png")

        while not self.task_manager.stop_event.is_set():
            coord_region = find_template_matches(path_region_btn)
            coord_shelter = find_template_matches(path_shelter_btn)
            if coord_region and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"GAME OBJECT SERVICE: REGION IN ACTION")
                self.clicker_manager.click(coord_region[0][0], coord_region[0][1])
                time.sleep(3)

            elif coord_shelter and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"GAME OBJECT SERVICE: SHELTER IN ACTION")
                break
            else:
                self.clicker_manager.press_ecs()
                time.sleep(3)

    @check_stop_func
    def go_to_region(self):
        logger.info(msg=f"GAME OBJECT SERVICE: CHECK REGION FUNC")
        path_region_btn = resource_path(relative_path="app\\img\\game_button\\go-region.png")
        path_shelter_btn = resource_path(relative_path="app\\img\\game_button\\go-shelter.png")

        while not self.task_manager.stop_event.is_set():
            if coord_region := find_template_matches(path_region_btn):
                logger.info(msg=f"GAME OBJECT SERVICE: REGION IN ACTION")
                break
            elif coord_shelter := find_template_matches(path_shelter_btn):
                logger.info(msg=f"GAME OBJECT SERVICE: SHELTER IN ACTION")
                self.clicker_manager.click(coord_shelter[0][0], coord_shelter[0][1])
                time.sleep(3)
            else:
                self.clicker_manager.press_ecs()
                time.sleep(3)

    def go_to_after_shift(self):
        logger.info(msg=f"GAME OBJECT SERVICE: GO TO AFTER SHIFT FUNC")
        path_region_btn = resource_path(relative_path="app\\img\\game_button\\go-region.png")
        path_shelter_btn = resource_path(relative_path="app\\img\\game_button\\go-shelter.png")

        while not self.task_manager.stop_event.is_set():
            coord_region = find_template_matches(path_region_btn)
            coord_shelter = find_template_matches(path_shelter_btn)
            if coord_region and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"GAME OBJECT SERVICE: REGION IN ACTION")
                self.clicker_manager.click(coord_region[0][0], coord_region[0][1])
                time.sleep(3)
                self.go_to_shelter()
                time.sleep(2)
                break
            elif coord_shelter and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"GAME OBJECT SERVICE: SHELTER IN ACTION")
                self.clicker_manager.click(coord_shelter[0][0], coord_shelter[0][1])
                time.sleep(3)
                self.go_to_region()
                time.sleep(2)
                self.go_to_shelter()
                time.sleep(2)
                break
            else:
                self.clicker_manager.press_ecs()
                time.sleep(3)
        return

    def hide_discont(self):
        logger.info(msg="GAME OBJECT SERVICE: HIDE DISCONT START")
        self.go_to_region()

        # path_zombi_icon = resource_path(relative_path="app\\img\\game_button\\zombi-war-icon.png")
        # coord_zombi_war_icon = find_template_matches(path_zombi_icon, threshold=0.8)
        # if coord_zombi_war_icon and not self.task_manager.stop_event.is_set():
        #     logger.info(msg="GAME OBJECT SERVICE: GET ZOMBI WAR EVENT")
        #     self.clicker_manager.click(coord_zombi_war_icon[0][0], coord_zombi_war_icon[0][1])
        #     time.sleep(3)
        #     self.clicker_manager.press_ecs()
        #     time.sleep(3)



        path_hide = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\hide_actions.png")
        coord_hide = find_template_matches(path_hide)
        if coord_hide:
            logger.info(msg="GAME OBJECT SERVICE: HIDE DISCONT BTN FIND")
            self.clicker_manager.click(coord_hide[0][0], coord_hide[0][1])
            time.sleep(1)
            self.go_to_shelter()
            time.sleep(3)
        else:
            logger.info(msg="GAME OBJECT SERVICE: HIDE DISCONT BTN UNDEFIND")
            self.go_to_shelter()



    @check_stop_func
    def buff_resourse(self):
        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - START CHECK RESOURSE BUFF")

        buff_food_8h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_food_8h.png")
        buff_food_24h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_food_24h.png")
        buff_wood_8h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_wood_8h.png")
        buff_wood_24h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_wood_24h.png")
        buff_steel_8h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_steel_8h.png")
        buff_steel_24h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_steel_24h.png")
        buff_oil_8h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_oil_8h.png")
        buff_oil_24h= resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_oil_24h.png")
        STATUS_FOOD_8H = False
        STATUS_FOOD_24H = False
        STATUS_WOOD_8H = False
        STATUS_WOOD_24H = False
        STATUS_STEEL_8H = False
        STATUS_STEEL_24H = False
        STATUS_OIL_8H = False
        STATUS_OIL_24H = False

        STATUS_FOOD = False
        STATUS_WOOD = False
        STATUS_STEAL = False
        STATUS_OIL = False

        coord_buff_food_8h = find_template_simple(buff_food_8h, threshold=0.8)
        if coord_buff_food_8h:
            STATUS_FOOD_8H = True
        coord_buff_food_24h = find_template_simple(buff_food_24h, threshold=0.8)
        if coord_buff_food_24h:
            STATUS_FOOD_24H = True

        if STATUS_FOOD_8H or STATUS_FOOD_24H:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - FOOD USED")
            STATUS_FOOD = True
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - FOOD NOT USED")

        coord_buff_wood_8h = find_template_simple(buff_wood_8h, threshold=0.8)
        if coord_buff_wood_8h:
            STATUS_WOOD_8H = True
        coord_buff_wood_24h = find_template_simple(buff_wood_24h, threshold=0.8)
        if coord_buff_wood_24h:
            STATUS_WOOD_24H = True

        if STATUS_WOOD_8H or STATUS_WOOD_24H:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - WOOD USED")
            STATUS_WOOD = True
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - WOOD NOT USED")

        coord_buff_steel_8h = find_template_simple(buff_steel_8h, threshold=0.8)
        if coord_buff_steel_8h:
            STATUS_STEEL_8H = True
        coord_buff_steel_24h = find_template_simple(buff_steel_24h, threshold=0.8)
        if coord_buff_steel_24h:
            STATUS_STEEL_24H = True

        if STATUS_STEEL_8H or STATUS_STEEL_24H:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - STEEL USED")
            STATUS_STEAL = True
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - STEEL NOT USED")

        coord_buff_oil_8h = find_template_simple(buff_oil_8h, threshold=0.8)
        if coord_buff_oil_8h:
            STATUS_OIL_8H = True
        coord_buff_oil_24h = find_template_simple(buff_oil_24h, threshold=0.8)
        if coord_buff_oil_24h:
            STATUS_OIL_24H = True

        if STATUS_OIL_8H or STATUS_OIL_24H:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - OIL USED")
            STATUS_OIL = True
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - OIL NOT USED")


        status_list = [STATUS_FOOD, STATUS_WOOD, STATUS_STEAL, STATUS_OIL]
        if any(not status for status in status_list):
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - START USE RESOURSE BUFF")
            bag_path = resource_path(relative_path="app\\img\\game_button\\bag.png")
            coord_bag = find_template_matches(bag_path, threshold=0.7)
            if coord_bag and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - BAG DETECTED")
                self.clicker_manager.click(coord_bag[0][0], coord_bag[0][1])
                time.sleep(4)
            else:
                logger.warning(msg="GAME OBJECT SERVICE: BUFF RESOURSE - BAG DONT DETECTED")
                self.go_to_shelter()
                return None
            coord_bag_buffs = []
            bag_buffs_path = resource_path(relative_path=self.locale.i10n('bag_buffs_button'))
            bag_buffs_path2 = resource_path(relative_path=self.locale.i10n('bag_buffs2_button'))
            bag_buffs_path3 = resource_path(relative_path=self.locale.i10n('bag_buffs3_button'))
            bag_buffs_path4 = resource_path(relative_path=self.locale.i10n('bag_buffs4_button'))
            bag_buffs_path5 = resource_path(relative_path=self.locale.i10n('bag_buffs5_button'))
            bag_fuffs_list = [
                bag_buffs_path,
                bag_buffs_path2,
                bag_buffs_path3,
                bag_buffs_path4,
                bag_buffs_path5,
            ]
            for path in bag_fuffs_list:
                time.sleep(0.5)
                coord_bag_buffs = find_template_matches(path, threshold=0.7)
                if coord_bag_buffs:
                    break
            if coord_bag_buffs and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - BUFF BUTTON IN BAG DETECTED")
                self.clicker_manager.click(coord_bag_buffs[0][0], coord_bag_buffs[0][1])
                time.sleep(4)
            else:
                logger.warning(msg="GAME OBJECT SERVICE: BUFF RESOURSE - BUFF MENU BUTTON IN BAG DONT DETECTED")
                self.go_to_shelter()
                return None

            coords_buff = []
            if not STATUS_FOOD:
                speedbuff_food_8h = resource_path(relative_path=self.locale.i10n('speedbuff_food_8h'))
                coord_speedbuff_food_8h = find_template_simple(speedbuff_food_8h, threshold=0.9)
                if coord_speedbuff_food_8h and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF FOOD 8H DETECTED")
                    coords_buff.append((coord_speedbuff_food_8h[0][0], coord_speedbuff_food_8h[0][1]))
                else:
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF FOOD 8H NOT DETECTED")
                    speedbuff_food_24h = resource_path(relative_path=self.locale.i10n('speedbuff_food_24h'))
                    coord_speedbuff_food_24h = find_template_simple(speedbuff_food_24h, threshold=0.9)
                    if coord_speedbuff_food_24h and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF FOOD 24H DETECTED")
                        coords_buff.append((coord_speedbuff_food_24h[0][0], coord_speedbuff_food_24h[0][1]))
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF FOOD 24H NOT DETECTED")
            if not STATUS_WOOD:
                speedbuff_wood_8h = resource_path(relative_path=self.locale.i10n('speedbuff_wood_8h'))
                coord_speedbuff_wood_8h = find_template_simple(speedbuff_wood_8h, threshold=0.9)
                if coord_speedbuff_wood_8h and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF WOOD 8H DETECTED")
                    coords_buff.append((coord_speedbuff_wood_8h[0][0], coord_speedbuff_wood_8h[0][1]))
                else:
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF WOOD 8H NOT DETECTED")
                    speedbuff_wood_24h = resource_path(relative_path=self.locale.i10n('speedbuff_wood_24h'))
                    coord_speedbuff_wood_24h = find_template_simple(speedbuff_wood_24h, threshold=0.9)
                    if coord_speedbuff_wood_24h and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF WOOD 24H DETECTED")
                        coords_buff.append((coord_speedbuff_wood_24h[0][0], coord_speedbuff_wood_24h[0][1]))
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF WOOD 24H NOT DETECTED")
            if not STATUS_STEAL:
                speedbuff_steel_8h = resource_path(relative_path=self.locale.i10n('speedbuff_steel_8h'))
                coord_speedbuff_steel_8h = find_template_simple(speedbuff_steel_8h, threshold=0.9)
                if coord_speedbuff_steel_8h and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF STEEL 8H DETECTED")
                    coords_buff.append((coord_speedbuff_steel_8h[0][0], coord_speedbuff_steel_8h[0][1]))
                else:
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF STEEL 8H NOT DETECTED")
                    speedbuff_steel_24h = resource_path(relative_path=self.locale.i10n('speedbuff_steel_24h'))
                    coord_speedbuff_steel_24h = find_template_simple(speedbuff_steel_24h, threshold=0.9)
                    if coord_speedbuff_steel_24h and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF STEEL 24H DETECTED")
                        coords_buff.append((coord_speedbuff_steel_24h[0][0], coord_speedbuff_steel_24h[0][1]))
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF STEEL 24H NOT DETECTED")
            if not STATUS_OIL:
                speedbuff_oil_8h = resource_path(relative_path=self.locale.i10n('speedbuff_oil_8h'))
                coord_speedbuff_oil_8h = find_template_simple(speedbuff_oil_8h, threshold=0.9)
                if coord_speedbuff_oil_8h and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF OIL 8H DETECTED")
                    coords_buff.append((coord_speedbuff_oil_8h[0][0], coord_speedbuff_oil_8h[0][1]))
                else:
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF OIL 8H NOT DETECTED")
                    speedbuff_oil_24h = resource_path(relative_path=self.locale.i10n('speedbuff_oil_24h'))
                    coord_speedbuff_oil_24h = find_template_simple(speedbuff_oil_24h, threshold=0.9)
                    if coord_speedbuff_oil_24h and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF OIL 24H DETECTED")
                        coords_buff.append((coord_speedbuff_oil_24h[0][0], coord_speedbuff_oil_24h[0][1]))
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SPEED BUFF OIL 24H NOT DETECTED")
            time.sleep(1)
            for x,y in coords_buff[::-1]:
                if self.task_manager.stop_event.is_set():
                    break
                logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - SELECT RESOURSE BUFF")
                self.clicker_manager.click(x=x, y=y)
                time.sleep(1)

                bag_use_path = resource_path(relative_path=self.locale.i10n('bag_buffs_use'))
                coord_bag_use = find_template_matches_color(bag_use_path, threshold=0.8)

                if coord_bag_use and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - USE BUTTON DETECTED")
                    self.clicker_manager.click(coord_bag_use[0][0], coord_bag_use[0][1])
                    time.sleep(1)

                    bag_cansel_use_buff_path = resource_path(relative_path=self.locale.i10n('bag_buffs_cancel'))
                    coord_bag_cansel_use_buff = find_template_matches_color(bag_cansel_use_buff_path, threshold=0.8)
                    if coord_bag_cansel_use_buff and not self.task_manager.stop_event.is_set():
                        self.clicker_manager.click(coord_bag_cansel_use_buff[0][0], coord_bag_cansel_use_buff[0][1])
                        time.sleep(2)
                        logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - BUFF THIS TYPE ALREADY USE")
                        self.clicker_manager.press_ecs()
                        time.sleep(1)
                else:
                    logger.warning(msg="GAME OBJECT SERVICE: BUFF RESOURSE - USE BTN DONT DETECTED")

            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - TASK END")
            self.go_to_shelter()
            time.sleep(2)
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF RESOURSE - ALL BUFFS USED")

    @check_stop_func
    def buff_gather(self):

        STATUS_BUFF_GATHER = False

        buff_gather_8h = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_gather_8h.png")
        coord_buff_gather_8h = find_template_simple(buff_gather_8h, threshold=0.7)
        if coord_buff_gather_8h:
            STATUS_BUFF_GATHER = True

        buff_gather_24h = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\buff_gather_24h.png")
        coord_buff_gather_24h = find_template_simple(buff_gather_8h, threshold=0.7)
        if coord_buff_gather_24h:
            STATUS_BUFF_GATHER = True

        if STATUS_BUFF_GATHER:
            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BUFF GATHER USED")
            return

        logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BUFF GATHER NOT USED")

        bag_path = resource_path(relative_path="app\\img\\game_button\\bag.png")
        coord_bag = find_template_matches(bag_path, threshold=0.7)
        if coord_bag:
            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BAG DETECTED")
            self.clicker_manager.click(coord_bag[0][0], coord_bag[0][1])
            time.sleep(4)
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BAG DONT DETECTED")
            self.go_to_shelter()
            return None

        coord_bag_buffs = []
        bag_buffs_path = resource_path(relative_path=self.locale.i10n('bag_buffs_button'))
        bag_buffs_path2 = resource_path(relative_path=self.locale.i10n('bag_buffs2_button'))
        bag_buffs_path3 = resource_path(relative_path=self.locale.i10n('bag_buffs3_button'))
        bag_buffs_path4 = resource_path(relative_path=self.locale.i10n('bag_buffs4_button'))
        bag_buffs_path5 = resource_path(relative_path=self.locale.i10n('bag_buffs5_button'))
        bag_fuffs_list = [
                bag_buffs_path,
                bag_buffs_path2,
                bag_buffs_path3,
                bag_buffs_path4,
                bag_buffs_path5,
            ]
        for path in bag_fuffs_list:
            time.sleep(0.5)
            coord_bag_buffs = find_template_matches(path, threshold=0.7)
            if coord_bag_buffs:
                break
        if coord_bag_buffs:
            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BUFF BUTTON IN BAG DETECTED")
            self.clicker_manager.click(coord_bag_buffs[0][0], coord_bag_buffs[0][1])
            time.sleep(4)
        else:
            self.go_to_shelter()
            return None

        coord = []

        sppedbuff_gather_8h = resource_path(relative_path=self.locale.i10n('speedbuff_gather_8h'))
        coord_speedbuff_gather_8h = find_template_matches_color(sppedbuff_gather_8h, threshold=0.7)

        if coord_speedbuff_gather_8h:
            coord = coord_speedbuff_gather_8h
        else:

            buff_gather_24h = resource_path(relative_path=self.locale.i10n('speedbuff_gather_24h'))
            coord_buff_gather_24h = find_template_simple(buff_gather_24h, threshold=0.7)

            if coord_buff_gather_24h:
                coord = coord_buff_gather_24h

        if coord:

            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - SPEED BUFF GATHER DETECTED")
            self.clicker_manager.click(coord[0][0], coord[0][1])
            time.sleep(1)

            bag_use_path = resource_path(relative_path=self.locale.i10n('bag_buffs_use'))
            coord_bag_use = find_template_matches_color(bag_use_path, threshold=0.8)

            if coord_bag_use:
                logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - USE BUTTON DETECTED")
                self.clicker_manager.click(coord_bag_use[0][0], coord_bag_use[0][1])
                time.sleep(1)

                bag_cansel_use_buff_path = resource_path(relative_path=self.locale.i10n('bag_buffs_cancel'))
                coord_bag_cansel_use_buff = find_template_matches_color(bag_cansel_use_buff_path, threshold=0.8)
                if coord_bag_cansel_use_buff:
                    self.clicker_manager.click(coord_bag_cansel_use_buff[0][0], coord_bag_cansel_use_buff[0][1])
                    time.sleep(2)
                    logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BUFF ALREADY USE")
                    self.go_to_shelter()
                    time.sleep(1)
                else:
                    self.go_to_shelter()
            else:
                self.go_to_shelter()
        else:
            logger.info(msg="GAME OBJECT SERVICE: BUFF GATHER - BUFF GATHER 8H OR 24H IN BAG DONT DETECTED")
            self.go_to_shelter()
        self.go_to_shelter()

# ==================== RADAR ================================= #
    def go_to_radar(self, window):
        logger.info(msg=f"GAME OBJECT SERVICE: GO TO RADAR FUNC")
        path_radar_btn = resource_path(relative_path="app\\img\\game_button\\radar.png")
        time.sleep(1)
        self.go_to_region()
        time.sleep(1)
        coord_radar = find_template_matches(path_radar_btn)
        if coord_radar:
            logger.info(msg=f"GAME OBJECT SERVICE: FIND RADAR BTN")
            self.clicker_manager.click(coord_radar[0][0], coord_radar[0][1])
            time.sleep(3)
        else:
            logger.warning(msg=f"GAME OBJECT SERVICE: RADAR BTN NOT FINDED. PROTORTIONAL RADAR CLICK")
            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=115, target_y=475)
            time.sleep(3)

    def check_radar_menu(self, window):
        path = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\radar_shop.png")
        coord = find_template_matches(path)
        if coord:
            logger.info(msg=f"RADAR: IN RADAR MENU")
            return True
        else:
            logger.info(msg=f"RADAR: NOT IN RADAR MENU")
            self.go_to_radar(window)

            coord = find_template_matches(path)
            if coord:
                return True
            return False


    def radar_user_task(self,window):
        logger.info(msg=f"RADAR: USER TASK STARTED")
        self.check_radar_menu(window)
        path_user_task = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\user_task.png")
        path_user_hand = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\user_hand.png")

        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))
        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        path_list_user = [
            path_user_task,
        ]

        if self.radar_task['car_task_count'] > 3:
            time.sleep(5)
            self.radar_task['car_task_count'] = 0

        for _ in range(7):
            if self.task_manager.stop_event.is_set():
                break

            coord_task = find_template_simple(path_user_task, threshold=0.7)
            time.sleep(0.5)

            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND USER TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                # Тут задание было найдено. Ищу кнопку вперёд чтоб его начать
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                    time.sleep(10)
                    # Ищу кнопку рука помощи
                    coord_user_hand = find_template_matches(path_user_hand)
                    if coord_user_hand and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: FIND BTN USER HAND")
                        self.clicker_manager.click(coord_user_hand[0][0], coord_user_hand[0][1])
                        time.sleep(3)
                    else:
                        # ТУТ скорее всего зночок был перекрыт банером ника или чем то
                        logger.info(msg=f"RADAR: DONT SEE USER HAND")
                        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=640, target_y=290)
                        time.sleep(3)
                        # Проверяю появилось ли окно то что нет энергии
                    coord_green_use = find_template_matches(path_green_use)
                    if coord_green_use and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: NO HAVE ENERGY")
                        green_count = 0
                        while not self.task_manager.stop_event.is_set():
                            if green_count == 15:
                                self.task_manager.stop_event.set()
                                return
                            coord_green_half = find_template_matches(path_green_half_empty)
                            if coord_green_half and not self.task_manager.stop_event.is_set():
                                coord_green_use_update = find_template_matches(path_green_use)
                                filter_coord = filter_coordinates(coord_green_use_update)
                                for x, y in filter_coord:
                                    self.clicker_manager.click(x, y)
                                    time.sleep(0.5)
                                green_count += 1
                            else:
                                self.clicker_manager.press_ecs()
                                time.sleep(2)
                                break
                        self.go_to_shelter()
                        time.sleep(2)
                        self.go_to_radar(window=window)
                        time.sleep(2)
                        continue
                    else:
                        logger.info(msg=f"RADAR: ENERGY IS GOOD")

                    self.radar_task['car_task_count'] += 1
                    self.radar_task['task_count'] += 1
                    logger.info("RADAR: TASK STARTED, COUNT TASK: %s", self.radar_task['car_task_count'])
                    self.go_to_shelter()
                    time.sleep(2)
                    self.go_to_radar(window=window)
                    time.sleep(2)
                    self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))
                    logger.info(msg="RADAR: TASK YEALD")
                    return
                    # else:
                    #     self.go_to_radar(window=window)
                    #     time.sleep(4)
                    #     continue
                # Тут Задание было найдено, но кнопки вперёд нету, потому что задание уже выполняется, нужно подождать появления кнопки ПОЛУЧИТЬ
                else:
                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")
                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        # Тут дополнительная проверка что есть надпись шанс, тем самым мы понимаем что мы в нужном меню ждём появления кнопки ПОЛУЧИТЬ
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)
            else:
                logger.info(msg=f"RADAR: USER TASK NOT FINDED")
                continue


        self.radar_task['user']['count'] += 1
        logger.info("RADAR: USER TASK ENDED: COUNT [%s]", self.radar_task['user']['count'])
        if self.radar_task['user']['count'] == 5:
            logger.info("RADAR: USER TASK FINISH")
            self.radar_task['user']['status_task'] = True
        return



    def check_end_radar(self):
        path = resource_path(relative_path=self.locale.i10n('radar-end'))
        coord = find_template_matches(path)
        if coord:
            logger.info(msg=f"RADAR: END ALL TASK")
            return True
        else:
            False

    def radar_zombi_car_dron_task(self, window):
        logger.info(msg=f"RADAR: ZOMBIE TASK STARTED")
        self.check_radar_menu(window)

        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_vpered2 = resource_path(relative_path=self.locale.i10n('radar-vpered-leg'))

        path_attack = resource_path(relative_path=self.locale.i10n('radar-attack'))
        path_check_box = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\fully_check_box.png")
        path_empty_check_box = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\empty_check_box.png")

        path_create_group = resource_path(relative_path=self.locale.i10n('radar-create-group'))
        path_marsh = resource_path(relative_path=self.locale.i10n('radar-marsh'))

        path_group_free_in_menu = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free_in_menu.png")

        path_marsh_in_free_group = resource_path(relative_path=self.locale.i10n('radar-marsh-free-group'))

        path_group_free = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free.png")
        path_group_free2 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free2.png")
        path_group_free3 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free3.png")
        path_group_free4 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free4.png")
        path_group_free5 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free5.png")
        path_group_free6 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free6.png")

        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))

        path_zombi_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\zombi_spec.png")
        path_zombi_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\zombi_rare.png")
        path_zombi_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\zombi_leg.png")
        path_zombi_leg2 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\zombi_leg2.png")
        path_car_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\car_spec.png")
        path_car_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\car_rare.png")
        path_dron_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\dron_spec.png")
        path_dron_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\dron_rare.png")
        path_action_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\action_rare.png")
        path_action_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\action_leg.png")
        path_bokal_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\bokal_rare.png")
        path_bokal_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\group_task\\bokal_leg.png")

        path_list = [
            path_zombi_spec,
            path_zombi_rare,
            path_zombi_leg,
            path_zombi_leg2,
            path_car_spec,
            path_car_rare,
            path_dron_spec,
            path_dron_rare,
            path_action_rare,
            path_action_leg,
            path_bokal_rare,
            path_bokal_leg
        ]

        NULL_TASK_COUNT = 0

        for path in path_list:
            # Ищу задачу
            if self.task_manager.stop_event.is_set():
                break
            coord_task = find_template_matches(path)
            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND ZOMBI TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                # Нашел задачу, ищу кнопку вперёд
                coord = []
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered:
                    coord = coord_vpered
                coord_vpered2 = find_template_matches(path_vpered2)
                if coord_vpered2:
                    coord = coord_vpered2
                # Проверяю нашел ли кнопку ВПЕРЕД
                if coord and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord[0][0], coord[0][1])
                    time.sleep(4)
                    # Ищу кнопку атаковать
                    coord_attack = find_template_matches(path_attack)
                    if coord_attack and not self.task_manager.stop_event.is_set():
                        # Нашел кнопку атаковать, проверяю стоит ли галочка чтобы отряд остался стоять в поле.
                        logger.info(msg=f"RADAR: FIND BTN ATTACK")
                        check_box_fully = find_template_matches(path_check_box, threshold=0.7)
                        if check_box_fully:
                            # Тут я убедился что галочка стоит
                            logger.info(msg=f"RADAR: CHECKBOX IS TRUE")
                            time.sleep(1)

                        else:
                            logger.info(msg=f"RADAR: CHECKBOX IS FALSE")
                            # Ищу пустой квадратик чтобы поставить галочку
                            coord_empty_checkbox = find_template_matches(path_empty_check_box, threshold=0.7)
                            if coord_empty_checkbox and not self.task_manager.stop_event.is_set():
                                logger.info(msg=f"RADAR: FIND EMPTY CHECKBOX")
                                self.clicker_manager.click(coord_empty_checkbox[0][0], coord_empty_checkbox[0][1])
                                time.sleep(1)
                            else:
                                logger.info(msg=f"RADAR: EMPTY CHECKBOX NOT FINDED")
                        # Нажимаю атаковать
                        logger.info(msg=f"RADAR: PRESS ATTACK BTN")
                        self.clicker_manager.click(coord_attack[0][0], coord_attack[0][1])
                        time.sleep(4)

                        # Проверяю есть ли отдыхающий отряд
                        coord_check_free_group = find_template_matches(path_group_free_in_menu)
                        if coord_check_free_group and not self.task_manager.stop_event.is_set():
                            self.clicker_manager.click(coord_check_free_group[0][0], coord_check_free_group[0][1])
                            time.sleep(1)
                            # Ищу кнопку Марш для отдыхающего отряда
                            coord_marsh_free_group = find_template_matches_color(path_marsh_in_free_group)
                            if coord_marsh_free_group and not self.task_manager.stop_event.is_set():
                                self.clicker_manager.click(coord_marsh_free_group[0][0], coord_marsh_free_group[0][1])
                                time.sleep(2)
                                self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))

                                # Проверяю появилось ли окно то нет энергии
                                coord_green_use = find_template_matches(path_green_use)
                                if coord_green_use and not self.task_manager.stop_event.is_set():
                                    logger.info(msg=f"RADAR: NO HAVE ENERGY")
                                    green_count = 0
                                    while not self.task_manager.stop_event.is_set():
                                        if green_count == 15:
                                            self.task_manager.stop_event.set()
                                            return
                                        coord_green_half = find_template_matches(path_green_half_empty)
                                        if coord_green_half and not self.task_manager.stop_event.is_set():
                                            coord_green_use_update = find_template_matches(path_green_use)
                                            filter_coord = filter_coordinates(coord_green_use_update)
                                            for x, y in filter_coord:
                                                self.clicker_manager.click(x, y)
                                                time.sleep(0.5)
                                            green_count += 1
                                        else:
                                            self.clicker_manager.press_ecs()
                                            time.sleep(1)
                                            self.clicker_manager.click(coord_marsh_free_group[0][0], coord_marsh_free_group[0][1])
                                            time.sleep(3)
                                            break
                                else:
                                    logger.info(msg=f"RADAR: ENERGY IS GOOD")

                                count_fail = 0
                                path_free_group_list = [
                                    path_group_free,
                                    path_group_free2,
                                    path_group_free3,
                                    path_group_free4,
                                    path_group_free5,
                                    path_group_free6
                                ]
                                while not self.task_manager.stop_event.is_set():
                                    # Тут я жду пока отряд убьет зомби или умрёт
                                    if count_fail > 40:
                                        break
                                    end_fight = []
                                    for path in path_free_group_list:
                                        end_fight = find_template_simple(path, threshold=0.7)
                                        if end_fight:
                                            break
                                    if end_fight and not self.task_manager.stop_event.is_set():
                                        logger.info(msg=f"RADAR: END FIGHT")
                                        self.radar_task['task_count'] += 1
                                        count_fail = 0
                                        break
                                    logger.info(msg=f"RADAR: WAIT END FIGHT")
                                    time.sleep(1.5)
                                    count_fail += 2
                                self.go_to_radar(window)
                        # Ищу кнопку Создать отряд
                        else:
                            coord_create_group = find_template_matches(path_create_group)
                            if coord_create_group and not self.task_manager.stop_event.is_set():
                                logger.info(msg=f"RADAR: CREATE GROUP BTN FIND")
                                self.clicker_manager.click(coord_create_group[0][0], coord_create_group[0][1])
                                time.sleep(3)
                                # Ищем кнопку Марш
                                coord_marsh = find_template_matches(path_marsh)
                                if coord_marsh and not self.task_manager.stop_event.is_set():
                                    logger.info(msg=f"RADAR: MARSH BTN FIND")
                                    self.clicker_manager.click(coord_marsh[0][0], coord_marsh[0][1])
                                    time.sleep(3)
                                    self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))



                                    # Проверяю появилось ли окно то нет энергии
                                    coord_green_use = find_template_matches(path_green_use)
                                    if coord_green_use and not self.task_manager.stop_event.is_set():
                                        logger.info(msg=f"RADAR: NO HAVE ENERGY")
                                        green_count = 0
                                        while not self.task_manager.stop_event.is_set():
                                            if green_count == 15:
                                                self.task_manager.stop_event.set()
                                                return
                                            coord_green_half = find_template_matches(path_green_half_empty)
                                            if coord_green_half and not self.task_manager.stop_event.is_set():
                                                coord_green_use_update = find_template_matches(path_green_use)
                                                filter_coord = filter_coordinates(coord_green_use_update)
                                                for x, y in filter_coord:
                                                    self.clicker_manager.click(x, y)
                                                    time.sleep(0.5)
                                                green_count += 1
                                            else:
                                                self.clicker_manager.press_ecs()
                                                time.sleep(1)
                                                self.clicker_manager.click(coord_marsh[0][0], coord_marsh[0][1])
                                                self.radar_task['task_count'] += 1
                                                time.sleep(3)
                                                break
                                    else:
                                        logger.info(msg=f"RADAR: ENERGY IS GOOD")

                                    count_fail = 0
                                    path_free_group_list = [
                                        path_group_free,
                                        path_group_free2,
                                        path_group_free3,
                                        path_group_free4,
                                        path_group_free5,
                                        path_group_free6
                                    ]
                                    while not self.task_manager.stop_event.is_set():
                                        # Тут я жду пока отряд убьет зомби или умрёт
                                        if count_fail > 40:
                                            break
                                        end_fight = []
                                        for path in path_free_group_list:
                                            end_fight = find_template_simple(path, threshold=0.7)
                                            if end_fight:
                                                break
                                        if end_fight and not self.task_manager.stop_event.is_set():
                                            logger.info(msg=f"RADAR: END FIGHT")
                                            self.radar_task['task_count'] += 1
                                            count_fail = 0
                                            break
                                        logger.info(msg=f"RADAR: WAIT END FIGHT")
                                        time.sleep(1.5)
                                        count_fail += 2
                                    self.go_to_radar(window)
                                else:
                                    # Тут почему то кнопка Марш недоступна
                                    logger.info(msg=f"RADAR: ZOMBI TASK MARSH NOT FINDED")
                                    self.go_to_radar(window)
                                    continue
                            else:
                                logger.warning(msg=f"RADAR: CREATE GROUP BTN NOT FINDED")
                                # тут почему то отряд не удалось создать
                                self.go_to_radar(window)
                                continue
                    else:
                        # Тут я не нашел кнопку атаковать
                        logger.info(msg=f"RADAR: ZOMBI TASK ATTACK NOT FINDED")
                        self.go_to_radar(window)
                        time.sleep(2)
                        continue
                # ТУТ НАШЕЛ ЗАДАЧУ НО НЕ НАШЕЛ КНОПКУ ВПЕРЁД
                else:
                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")

                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        # Тут дополнительная проверка что есть надпись шанс, тем самым мы понимаем что мы в нужном меню ждём появления кнопки ПОЛУЧИТЬ
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)
            #Тут я не нашел задачу
            else:
                logger.info(msg=f"RADAR: ZOMBI TASK NOT FINDED")
                time.sleep(1)
                NULL_TASK_COUNT += 1
                continue

        if NULL_TASK_COUNT == 8:
            self.radar_task['zombi']['null_status'] = True
            logger.info("RADAR: ZOMBI TASK NULL STATUS UP TO:%s", self.radar_task['zombi']['null_status'])

        self.radar_task['zombi']['count'] += 1
        logger.info("RADAR: ZOMBI TASK ENDED: COUNT [%s]", self.radar_task['zombi']['count'])
        if self.radar_task['zombi']['count'] == 5:
            logger.info("RADAR: ZOMBI TASK FINISH")
            self.radar_task['zombi']['status_task'] = True
        return

    def radar_drop_task(self,window):
        logger.info(msg=f"RADAR: DROP TASK STARTED")
        self.check_radar_menu(window)
        path_drop_imp = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\drop_imp.png")
        path_drop_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\drop_leg.png")
        path_drop_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\drop_rare.png")
        path_drop_rare2 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\drop_rare2.png")
        path_drop_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\drop_spec.png")

        path_sobrat_drop = resource_path(relative_path=self.locale.i10n('radar-sobrat-drop'))
        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))
        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        NULL_TASK_COUNT = 0

        path_list_drop = [
            path_drop_imp,
            path_drop_leg,
            path_drop_rare,
            path_drop_rare2,
            path_drop_spec
        ]

        if self.radar_task['car_task_count'] > 3:
            time.sleep(5)
            self.radar_task['car_task_count'] = 0

        for path in path_list_drop:
            time.sleep(1)
            if self.task_manager.stop_event.is_set():
                break
            coord_task = find_template_matches(path, threshold=0.7)
            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND DROP CAR TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                # Тут задание было найдено. Ищу кнопку вперёд чтоб его начать
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                    time.sleep(6)
                    coord_sobrat_drop = find_template_matches(path_sobrat_drop)
                    if coord_sobrat_drop and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: FIND BTN SOBRAT")
                        self.clicker_manager.click(coord_sobrat_drop[0][0], coord_sobrat_drop[0][1])
                        time.sleep(2)

                        # Проверяю появилось ли окно то что нет энергии
                        coord_green_use = find_template_matches(path_green_use)
                        if coord_green_use and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: NO HAVE ENERGY")
                            green_count = 0
                            while not self.task_manager.stop_event.is_set():
                                if green_count == 15:
                                    self.task_manager.stop_event.set()
                                    return
                                coord_green_half = find_template_matches(path_green_half_empty)
                                if coord_green_half and not self.task_manager.stop_event.is_set():
                                    coord_green_use_update = find_template_matches(path_green_use)
                                    filter_coord = filter_coordinates(coord_green_use_update)
                                    for x, y in filter_coord:
                                        self.clicker_manager.click(x, y)
                                        time.sleep(0.5)
                                    green_count += 1
                                else:
                                    self.clicker_manager.press_ecs()
                                    time.sleep(2)
                                    break
                            self.go_to_radar(window=window)
                            continue
                        else:
                            logger.info(msg=f"RADAR: ENERGY IS GOOD")



                        self.radar_task['car_task_count'] += 1
                        self.radar_task['task_count'] += 1
                        logger.info("RADAR: TASK STARTED, COUNT TASK: %s", self.radar_task['car_task_count'])
                        self.go_to_radar(window=window)
                        time.sleep(2)
                        self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))
                        logger.info(msg="RADAR: DROP TASK YEALD")
                        return
                    else:
                        self.go_to_radar(window=window)
                        time.sleep(4)
                        continue
                # Тут Задание было найдено, но кнопки вперёд нету, потому что задание уже выполняется, нужно подождать появления кнопки ПОЛУЧИТЬ
                else:
                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")

                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        # Тут дополнительная проверка что есть надпись шанс, тем самым мы понимаем что мы в нужном меню ждём появления кнопки ПОЛУЧИТЬ
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)
            else:
                logger.info(msg=f"RADAR: DROP TASK NOT FINDED")
                NULL_TASK_COUNT += 1
                continue

        if NULL_TASK_COUNT == 5:
            self.radar_task['drop']['null_status'] = True
            logger.info("RADAR: DROP TASK NULL STATUS UP TO:%s", self.radar_task['drop']['null_status'])

        self.radar_task['drop']['count'] += 1
        logger.info("RADAR: DROP TASK ENDED: COUNT [%s]", self.radar_task['drop']['count'])
        if self.radar_task['drop']['count'] == 5:
            logger.info("RADAR: DROP TASK FINISH")
            self.radar_task['drop']['status_task'] = True
        return

    def radar_ppl_task(self,window):
        logger.info(msg=f"RADAR: PPL TASK STARTED")
        self.check_radar_menu(window)
        path_ppl_imp = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\ppl_imp.png")
        path_ppl_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\ppl_leg.png")
        path_ppl_leg2 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\ppl_leg2.png")
        path_ppl_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\ppl_spec.png")

        path_ppl_save = resource_path(relative_path=self.locale.i10n('radar-ppl-save'))

        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))
        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        NULL_TASK_COUNT = 0

        path_list_ppl = [
            path_ppl_imp,
            path_ppl_leg,
            path_ppl_leg2,
            path_ppl_spec
        ]

        if self.radar_task['car_task_count'] > 3:
            time.sleep(5)
            self.radar_task['car_task_count'] = 0

        for path in path_list_ppl:
            time.sleep(0.5)
            if self.task_manager.stop_event.is_set():
                break

            coord_task = find_template_matches(path, threshold=0.7)
            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND PPL CAR TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                # Тут задание было найдено. Ищу кнопку вперёд чтоб его начать
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                    time.sleep(6)
                    coord_save_ppl = find_template_matches(path_ppl_save)
                    if coord_save_ppl and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: FIND BTN SOBRAT")
                        self.clicker_manager.click(coord_save_ppl[0][0], coord_save_ppl[0][1])
                        time.sleep(3)
                        # Проверяю появилось ли окно то что нет энергии
                        coord_green_use = find_template_matches(path_green_use)
                        if coord_green_use and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: NO HAVE ENERGY")
                            green_count = 0
                            while not self.task_manager.stop_event.is_set():
                                if green_count == 15:
                                    self.task_manager.stop_event.set()
                                    return
                                coord_green_half = find_template_matches(path_green_half_empty)
                                if coord_green_half and not self.task_manager.stop_event.is_set():
                                    coord_green_use_update = find_template_matches(path_green_use)
                                    filter_coord = filter_coordinates(coord_green_use_update)
                                    for x, y in filter_coord:
                                        self.clicker_manager.click(x, y)
                                        time.sleep(0.5)
                                    green_count += 1
                                else:
                                    self.clicker_manager.press_ecs()
                                    time.sleep(2)
                                    break
                            self.go_to_radar(window=window)
                            time.sleep(2)
                            continue
                        else:
                            logger.info(msg=f"RADAR: ENERGY IS GOOD")

                        self.radar_task['car_task_count'] += 1
                        self.radar_task['task_count'] += 1
                        logger.info("RADAR: TASK STARTED, COUNT TASK: %s", self.radar_task['car_task_count'])
                        self.go_to_radar(window=window)
                        time.sleep(2)
                        self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))
                        logger.info(msg="RADAR: TASK YEALD")
                        return
                    else:
                        self.go_to_radar(window=window)
                        time.sleep(4)
                        continue
                # Тут Задание было найдено, но кнопки вперёд нету, потому что задание уже выполняется, нужно подождать появления кнопки ПОЛУЧИТЬ
                else:
                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")
                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        # Тут дополнительная проверка что есть надпись шанс, тем самым мы понимаем что мы в нужном меню ждём появления кнопки ПОЛУЧИТЬ
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)
            else:
                logger.info(msg=f"RADAR: PPL TASK NOT FINDED")
                NULL_TASK_COUNT += 1
                continue

        if NULL_TASK_COUNT == 4:
            self.radar_task['ppl']['null_status'] = True
            logger.info("RADAR: PPL TASK NULL STATUS UP TO:%s", self.radar_task['ppl']['null_status'])


        self.radar_task['ppl']['count'] += 1
        logger.info("RADAR: PPL TASK ENDED: COUNT [%s]", self.radar_task['ppl']['count'])
        if self.radar_task['ppl']['count'] == 5:
            logger.info("RADAR: PPL TASK FINISH")
            self.radar_task['ppl']['status_task'] = True
        return

    def radar_kamaz_task(self,window):
        logger.info(msg=f"RADAR: KAMAZ TASK STARTED")
        self.check_radar_menu(window)
        path_kamaz_imp = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\kamaz_imp.png")
        path_kamaz_leg = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\kamaz_leg.png")
        path_kamaz_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\kamaz_rare.png")
        path_kamaz_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\kamaz_spec.png")

        path_transport = resource_path(relative_path=self.locale.i10n('radar-transport'))
        path_transport_ok = resource_path(relative_path=self.locale.i10n('radar-transport-ok'))

        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))
        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        NULL_TASK_COUNT = 0

        path_list_kamaz = [
            path_kamaz_imp,
            path_kamaz_leg,
            path_kamaz_rare,
            path_kamaz_spec
        ]

        if self.radar_task['car_task_count'] > 3:
            time.sleep(10)
            self.radar_task['car_task_count'] = 0

        for path in path_list_kamaz:
            time.sleep(0.5)
            if self.task_manager.stop_event.is_set():
                break
            coord_task = find_template_matches(path, threshold=0.7)
            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND KAMAZ CAR TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                #Тут нашло задание. ищу кнопку ВПЕРЕД
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                    time.sleep(6)
                    coord_transport_kamaz = find_template_matches(path_transport)
                    # Тут Ищу кноку транспортировать
                    if coord_transport_kamaz and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: FIND BTN TRANSPORTIROVAT")
                        self.clicker_manager.click(coord_transport_kamaz[0][0], coord_transport_kamaz[0][1])
                        time.sleep(2)
                        # Проверяю появилось ли окно то что нет энергии
                        coord_green_use = find_template_matches(path_green_use)
                        if coord_green_use and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: NO HAVE ENERGY")
                            green_count = 0
                            while not self.task_manager.stop_event.is_set():
                                if green_count == 15:
                                    self.task_manager.stop_event.set()
                                    return
                                coord_green_half = find_template_matches(path_green_half_empty)
                                if coord_green_half and not self.task_manager.stop_event.is_set():
                                    coord_green_use_update = find_template_matches(path_green_use)
                                    filter_coord = filter_coordinates(coord_green_use_update)
                                    for x, y in filter_coord:
                                        self.clicker_manager.click(x, y)
                                        time.sleep(0.5)
                                    green_count += 1
                                else:
                                    self.clicker_manager.press_ecs()
                                    time.sleep(2)
                                    break
                            self.go_to_radar(window=window)
                            time.sleep(2)
                            continue
                        else:
                            logger.info(msg=f"RADAR: ENERGY IS GOOD")
                        # Тут ищу кнопку ОК т.к требуется взнос ресурсов
                        coord_transport_ok_kamaz = find_template_matches(path_transport_ok)
                        if coord_transport_ok_kamaz and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: FIND BTN OK")
                            self.clicker_manager.click(coord_transport_ok_kamaz[0][0], coord_transport_ok_kamaz[0][1])
                            self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))
                            self.radar_task['car_task_count'] += 1
                            self.radar_task['task_count'] += 1
                            logger.info("RADAR: TASK STARTED, COUNT TASK: %s", self.radar_task['car_task_count'])
                            self.go_to_radar(window=window)
                            time.sleep(2)
                            logger.info(msg="RADAR: KAMAZ TASK YEALD")
                            return
                        else:
                            # Нужно словить момент когда ресурсов будет не хватать
                            logger.info(msg=f"RADAR: NOT FIND BTN OK")
                            self.go_to_radar(window=window)
                            time.sleep(2)
                            continue

                    else:
                        self.go_to_radar(window=window)
                        time.sleep(4)
                        continue
                # Тут нажалось на задание, но кнопку ВПЕРЕД не нашло, нужно подождать пока задание завершится.
                else:

                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")
                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)
            # Тут не нашло задание
            else:
                logger.info(msg="RADAR: KAMAZ TASK NOT FINDED")
                NULL_TASK_COUNT += 1
                continue

        if NULL_TASK_COUNT == 4:
            self.radar_task['kamaz']['null_status'] = True
            logger.info("RADAR: KAMAZ TASK NULL STATUS UP TO:%s", self.radar_task['kamaz']['null_status'])

        self.radar_task['kamaz']['count'] += 1
        logger.info("RADAR: KAMAZ TASK ENDED: COUNT [%s]", self.radar_task['kamaz']['count'])
        if self.radar_task['kamaz']['count'] == 5:
            logger.info("RADAR: KAMAZ TASK FINISH")
            self.radar_task['kamaz']['status_task'] = True
        return

    def radar_card_task(self,window):
        logger.info(msg=f"RADAR: CARD TASK STARTED")
        self.check_radar_menu(window)
        path_card_rare = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\card_rare.png")
        path_card_spec = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\car_task\\card_spec.png")

        path_save = resource_path(relative_path=self.locale.i10n('radar-save-card'))

        path_vpered = resource_path(relative_path=self.locale.i10n('radar-vpered'))
        path_get_task = resource_path(relative_path=self.locale.i10n('radar-get-task'))
        path_get_task_chanse = resource_path(relative_path=self.locale.i10n('radar-get-task-chanse'))
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")

        NULL_TASK_COUNT = 0

        path_list_card = [
            path_card_rare,
            path_card_spec,

        ]

        if self.radar_task['car_task_count'] > 3:
            time.sleep(10)
            self.radar_task['car_task_count'] = 0

        for path in path_list_card:
            if self.task_manager.stop_event.is_set():
                break
            time.sleep(0.5)

            coord_task = find_template_matches(path, threshold=0.7)
            if coord_task and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"RADAR: FIND CAR TASK")
                self.clicker_manager.click(coord_task[0][0], coord_task[0][1])
                time.sleep(3)
                coord_vpered = find_template_matches(path_vpered)
                if coord_vpered and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"RADAR: FIND BTN VPERED")
                    self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                    time.sleep(6)
                    coord_save = find_template_matches(path_save)
                    if coord_save and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"RADAR: FIND BTN TRANSPORTIROVAT")
                        self.clicker_manager.click(coord_save[0][0], coord_save[0][1])
                        time.sleep(3)
                        # Проверяю появилось ли окно то что нет энергии
                        coord_green_use = find_template_matches(path_green_use)
                        if coord_green_use and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: NO HAVE ENERGY")
                            green_count = 0
                            while not self.task_manager.stop_event.is_set():
                                if green_count == 15:
                                    self.task_manager.stop_event.set()
                                    return
                                coord_green_half = find_template_matches(path_green_half_empty)
                                if coord_green_half and not self.task_manager.stop_event.is_set():
                                    coord_green_use_update = find_template_matches(path_green_use)
                                    filter_coord = filter_coordinates(coord_green_use_update)
                                    for x, y in filter_coord:
                                        self.clicker_manager.click(x, y)
                                        time.sleep(0.5)
                                    green_count += 1
                                else:
                                    self.clicker_manager.press_ecs()
                                    time.sleep(2)
                                    break
                            self.go_to_radar(window=window)
                            time.sleep(2)
                            continue
                        else:
                            logger.info(msg=f"RADAR: ENERGY IS GOOD")

                        self.radar_task['task_coord'].append((coord_task[0][0], coord_task[0][1], datetime.datetime.now()))
                        time.sleep(3)
                        self.radar_task['car_task_count'] += 1
                        self.radar_task['task_count'] += 1
                        logger.info("RADAR: TASK STARTED, COUNT TASK: %s", self.radar_task['car_task_count'])
                        self.go_to_radar(window=window)
                        time.sleep(1)
                        logger.info(msg="RADAR: CARD TASK YEALD")
                        return

                    else:
                        self.go_to_radar(window=window)
                        time.sleep(3)
                        continue
                else:
                    logger.info(msg=f"RADAR: BTN VPERED NOT FINDED")
                    while not self.task_manager.stop_event.is_set():
                        coord_chanse = find_template_matches(path_get_task_chanse)
                        if coord_chanse:
                            pass
                        else:
                            break
                        coord_get_task = find_template_matches(path_get_task)
                        if coord_get_task and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"RADAR: BTN GET TASK IN ACTION")
                            self.clicker_manager.click(coord_get_task[0][0], coord_get_task[0][1])
                            time.sleep(4)
                            break
                        logger.info(msg=f"RADAR: WAIT BTN GET TASK")
                        time.sleep(5)

            else:
                logger.info(msg=f"RADAR: CARD TASK NOT FINDED")
                NULL_TASK_COUNT += 1
                continue

        if NULL_TASK_COUNT == 2:
            self.radar_task['card']['null_status'] = True
            logger.info("RADAR: CARD TASK NULL STATUS UP TO:%s", self.radar_task['card']['null_status'])


        self.radar_task['card']['count'] += 1
        logger.info("RADAR: CARD TASK ENDED: COUNT [%s]", self.radar_task['card']['count'])
        if self.radar_task['card']['count'] == 5:
            logger.info("RADAR: CARD TASK FINISH")
            self.radar_task['card']['status_task'] = True
        return

    def back_first_group_home(self):

        logger.info(msg="GAME OBJECT SERVICE:BACK FIRST GROUP HOME FUNC STARTED")
        path_group_menu = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_menu.png")
        path_group_go_home = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_go_home.png")

        self.go_to_region()
        time.sleep(2)
        coord_group_menu = find_template_matches(path_group_menu)
        if coord_group_menu and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: GO GROUP MENU")
            self.clicker_manager.click(coord_group_menu[0][0], coord_group_menu[0][1])
            time.sleep(3)

            coord_group_go_home = find_template_matches(path_group_go_home)
            highest = min(coord_group_go_home, key=lambda coord: coord[1])
            if highest and not self.task_manager.stop_event.is_set():
                self.clicker_manager.click(highest[0], highest[1])
                logger.info(msg="GAME OBJECT SERVICE: FIRST GROUP GO HOME")
                time.sleep(2)
                path_back_ok = resource_path(self.locale.i10n('back-troops-ok'))
                coord_back_ok = find_template_matches(path_back_ok)
                if coord_back_ok and not self.task_manager.stop_event.is_set():
                    self.clicker_manager.click(coord_back_ok[0][0], coord_back_ok[0][1])
                    time.sleep(2)
                self.go_to_region()
            else:
                logger.info(msg="GAME OBJECT SERVICE: BTN BACK GROUP UNDEFIND")
        else:
            logger.info(msg="GAME OBJECT SERVICE: GROUP MENU UNDEFIND")

    def back_all_group_home(self):

        logger.info(msg="GAME OBJECT SERVICE:BACK ALL GROUP HOME STARTED")
        path_group_menu = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_menu.png")
        path_group_go_home = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_go_home.png")

        self.go_to_region()
        time.sleep(2)
        coord_group_menu = find_template_matches(path_group_menu)
        if coord_group_menu and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: GO GROUP MENU")
            self.clicker_manager.click(coord_group_menu[0][0], coord_group_menu[0][1])
            time.sleep(3)
            times = 0
            while not self.task_manager.stop_event.is_set():
                if times == 4:
                    break
                coord_group_go_home = find_template_matches(path_group_go_home)
                filter_coord = filter_coordinates(coords=coord_group_go_home, threshold=10)
                for coord in filter_coord:
                    self.clicker_manager.click(coord[0], coord[1])
                    logger.info(msg="GAME OBJECT SERVICE: GROUP GO HOME")
                    time.sleep(5)
                    path_back_ok = resource_path(self.locale.i10n('back-troops-ok'))
                    coord_back_ok = find_template_matches(path_back_ok)
                    if coord_back_ok and not self.task_manager.stop_event.is_set():
                        self.clicker_manager.click(coord_back_ok[0][0], coord_back_ok[0][1])
                        time.sleep(2)

                times += 1
                self.clicker_manager.scroll(target=-25)
                time.sleep(2)

            self.go_to_region()
        else:
            logger.info(msg="GAME OBJECT SERVICE: GROUP MENU UNDEFIND")

    def check_free_group(self):
        logger.info(msg="GAME OBJECT SERVICE: CHECK MAX GROUPS FUNC")
        path_55 = resource_path(relative_path="app\\img\\game_button\\55.png")
        path_44 = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\44.png")
        path_33 = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\33.png")
        # path_zombi_icon = resource_path(relative_path="app\\img\\game_button\\zombi-war-icon.png")
        find_coord_list = []
        path_list = [
            path_55,
            path_44,
            path_33
        ]

        # coord_zombi_war_icon = find_template_matches(path_zombi_icon, threshold=0.8)
        # if coord_zombi_war_icon and not self.task_manager.stop_event.is_set():
        #     logger.info(msg="GAME OBJECT SERVICE: GET ZOMBI WAR EVENT")
        #     self.clicker_manager.click(coord_zombi_war_icon[0][0], coord_zombi_war_icon[0][1])
        #     time.sleep(3)
        #     self.clicker_manager.press_ecs()
        #     time.sleep(3)


        for path in path_list:
            if not self.task_manager.stop_event.is_set():
                get_troops = find_template_matches(path, threshold=0.95)
                find_coord_list.extend(get_troops)
            else:
                break

        if find_coord_list and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: SEE MAX GROUPS -  ALL GROUPS USED")
            return False
        logger.info(msg="GAME OBJECT SERVICE: GET FREE GROUP")
        return True

    def check_free_one_group(self):
        logger.info(msg="GAME OBJECT SERVICE: CHECK MAX GROUPS FUNC")
        path_45 = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\45.png")
        path_34 = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\34.png")
        # path_23 = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\33.png")
        find_coord_list = []
        path_list = [
            path_45,
            path_34,
            # path_23
        ]
        for path in path_list:
            if not self.task_manager.stop_event.is_set():
                get_troops = find_template_matches(path, threshold=0.95)
                find_coord_list.extend(get_troops)
            else:
                break

        if find_coord_list and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: SEE MAX GROUPS -  ALL GROUPS USED")
            return False
        logger.info(msg="GAME OBJECT SERVICE: GET FREE GROUP")
        return True


    def radar_algorithm(self, window):
        NULL_COUNT = 0
        self.radar_task = {
            "user": {"status_task": False,
                      "count": 0,
                      "func": self.radar_user_task,
            },
            "zombi": {"status_task": False,
                      "count": 0,
                      "null_status": False,
                      "func": self.radar_zombi_car_dron_task
            },
            "drop": {"status_task": False,
                     "count": 0,
                     "null_status": False,
                      "func": self.radar_drop_task
            },
            "ppl": {"status_task": False,
                    "count": 0,
                    "null_status": False,
                    "func": self.radar_ppl_task
            },
            "kamaz": {"status_task": False,
                      "count": 0,
                      "null_status": False,
                      "func": self.radar_kamaz_task
            },
            "card": {"status_task": False,
                     "count": 0,
                     "null_status": False,
                    "func": self.radar_card_task
            },

            "car_task_count": 0,
            "task_coord": [],
            "task_count": 0
        }

        if self.check_free_group():
            logger.info(msg=f"RADAR: HAVE FREE TROOPS")
            pass
        else:
            logger.info(msg=f"RADAR: ALL TROOPS BUSY")
            self.back_all_group_home()
            logger.info(msg=f"RADAR: WAIT 30 SEC BACK TROOPS TO HOME")
            time.sleep(30)

        self.go_to_region()
        time.sleep(2)
        self.hide_discont()
        time.sleep(1)
        if self.check_radar_menu(window):
            logger.info(msg=f"RADAR: GO RADAR LOOP")
            if self.check_end_radar():
                return None
            loop_started = datetime.datetime.now()

            while not self.task_manager.stop_event.is_set():
                # Проверяем все ли задания завершены
                self.task_manager.app.validator.get_time()
                if self.check_end_radar():
                    break

                for i in range(5):
                    path_get_end_task = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\red_spot.png")
                    coord_end_task = find_template_simple(path_get_end_task, threshold=0.7)
                    if coord_end_task:
                        filters_end_task = filter_coordinates(coords=coord_end_task)
                        for x,y in filters_end_task:
                            logger.info(msg="RADAR: FIND FINISHED TASK")
                            self.clicker_manager.click(x, y)
                            time.sleep(1)
                    time.sleep(0.7)

                if not self.radar_task['user']['status_task'] and self.radar_task['user']['count'] <= 6 and not self.task_manager.stop_event.is_set():
                    self.radar_user_task(window)
                else:
                    logger.info(msg="RADAR: USER TASKS COMPLETE")

                if not self.radar_task['zombi']['status_task'] and self.radar_task['zombi']['count'] <= 6 and not self.task_manager.stop_event.is_set():
                    self.radar_zombi_car_dron_task(window)
                else:
                    logger.info(msg="RADAR: ZOMBI TASKS COMPLETE")

                if not self.radar_task['ppl']['status_task'] and self.radar_task['ppl']['count'] <= 5 and not self.task_manager.stop_event.is_set():
                    self.radar_ppl_task(window)
                else:
                    logger.info(msg="RADAR: PPL TASKS COMPLETE")

                if not self.radar_task['card']['status_task'] and self.radar_task['card']['count'] <= 5 and not self.task_manager.stop_event.is_set():
                    self.radar_card_task(window=window)
                else:
                    logger.info(msg="RADAR: CARD TASKS COMPLETE")

                if not self.radar_task['kamaz']['status_task'] and self.radar_task['kamaz']['count'] <= 5 and not self.task_manager.stop_event.is_set():
                    self.radar_kamaz_task(window=window)
                else:
                    logger.info(msg=f"RADAR: KAMAZ TASKS COMPLETE")

                if not self.radar_task['drop']['status_task'] and self.radar_task['drop']['count'] <= 5 and not self.task_manager.stop_event.is_set():
                    self.radar_drop_task(window=window)
                else:
                    logger.info(msg="RADAR: DROP TASKS COMPLETE")

                if self.radar_task['task_coord']:
                    self.check_radar_menu(window)

                    for i in range(len(self.radar_task['task_coord'])-1, -1, -1):
                        x, y, timest = self.radar_task['task_coord'][i]
                        difference = abs((datetime.datetime.now() - timest).total_seconds())
                        if difference > 40 and not self.task_manager.stop_event.is_set():
                            del self.radar_task['task_coord'][i]
                            logger.info(msg="RADAR: GET TASK")
                            self.clicker_manager.click(x=x, y=y)
                            time.sleep(1)

                if all([self.radar_task['kamaz']['null_status'], self.radar_task['card']['null_status'], self.radar_task['drop']['null_status'], self.radar_task['zombi']['null_status']]):
                    NULL_COUNT += 1
                    logger.info("RADAR: NULL STATUS UP TO:%s", NULL_COUNT)
                    if NULL_COUNT >= 2:
                        logger.info(msg="RADAR: NULL STATUS CONFIM")
                        break
                else:
                    logger.info(msg="RADAR: NULL STATUS DROP")
                    self.radar_task['kamaz']['null_status'] = False
                    self.radar_task['card']['null_status'] = False
                    self.radar_task['drop']['null_status'] = False
                    self.radar_task['zombi']['null_status'] = False


                if all([self.radar_task['kamaz']['status_task'], self.radar_task['card']['status_task'], self.radar_task['drop']['status_task'], self.radar_task['zombi']['status_task'], self.radar_task['user']['status_task']]):
                    logger.info(msg="RADAR: MAX COUNT CHECK TASK - LOOP BREAK.")
                    break

            self.back_all_group_home()
            loop_end = datetime.datetime.now()
            # Вычисляем затраченное время
            elapsed_time = loop_end - loop_started

            # Получаем минуты и секунды
            minutes, seconds = divmod(elapsed_time.total_seconds(), 60)

            # Логируем информацию
            logger.info("RADAR: LOOP FINISH. TASK COMPLETED: %s. TIME TAKEN: %dm %ds",
                        self.radar_task['task_count'],
                        int(minutes),
                        int(seconds))
            self.radar_task = {}





# ============================= DAILY ============================= #
    @check_stop_func
    def click_hand(self):
        hand_path = resource_path(relative_path="app\\img\\game_button\\hand.png")
        coord_hand = find_template_matches(hand_path, threshold=0.7)
        if coord_hand:
            logger.info(msg="GAME OBJECT SERVICE: CLICK HAND")
            self.clicker_manager.click(coord_hand[0][0], coord_hand[0][1])
            time.sleep(2)
        else:
            logger.info(msg="GAME OBJECT SERVICE: HAND NOT DEFIENED")

    @check_stop_func
    def take_vip(self, window):
        # Клик по значку VIP
        logger.info(msg="GAME OBJECT SERVICE: TAKE VIP BONUS STARTED")
        self.clicker_manager.proportion_click_in_window(window=window.window,target_x=120, target_y=95)
        time.sleep(3)
        get_chest_path = resource_path(relative_path=self.locale.i10n('vip-get-chest'))
        coord_get_chest = find_template_matches(get_chest_path)
        if coord_get_chest and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE VIP: GET CHEST BOUNS")
            self.clicker_manager.click(coord_get_chest[0][0], coord_get_chest[0][1])
            time.sleep(3)
            self.clicker_manager.click_at_current_position()
            time.sleep(3)
        else:
            logger.info(msg="GAME OBJECT SERVICE: TAKE VIP: GET CHEST BOUNS UNDEFIND")

        get_card_path = resource_path(relative_path=self.locale.i10n('vip-get-card'))
        coord_get_card = find_template_matches(get_card_path)
        if coord_get_card and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE VIP: GET CARD BOUNS")

            self.clicker_manager.click(coord_get_card[0][0], coord_get_card[0][1])
            time.sleep(2)
            self.clicker_manager.press_ecs()
        else:
            logger.info(msg="GAME OBJECT SERVICE: TAKE VIP: GET CARD BOUNS UNDEFIND")

        self.go_to_shelter()

    @check_stop_func
    def take_police_dron(self, window):
        get_dron = resource_path(relative_path="app\\img\\game_button\\police_dron.png")
        coord_dron = []
        for _ in range(7):
            coord_dron = find_template_matches(get_dron)
            if coord_dron:
                break

        if coord_dron and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: FIND DRON")
            self.clicker_manager.click(coord_dron[0][0], coord_dron[0][1])
            time.sleep(3)
            path_dron_get = resource_path(relative_path=self.locale.i10n('dron-get'))
            coord_get = find_template_matches_color(path_dron_get)
            if coord_get:
                logger.info(msg="GAME OBJECT SERVICE: FIND GET DRON BTN")
                self.clicker_manager.click(coord_get[0][0], coord_get[0][1])
                time.sleep(10)
        self.go_to_shelter()

    @check_stop_func
    def police_poisk(self):
        police_path = resource_path(relative_path=self.locale.i10n('police-title-build1'))
        police_path2 = resource_path(relative_path=self.locale.i10n('police-title-build2'))
        police_path = [
            police_path,
            police_path2
        ]
        coord_police = []
        for path in police_path:
            coord = find_template_matches_color(path, threshold=0.7)
            if coord:
                coord_police = coord
                break
        # Ищу значок поиск над зданием
        if coord_police and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: Police BUILD DETECTED")
            self.clicker_manager.click(coord_police[0][0], coord_police[0][1])
            time.sleep(3)
            police_poisk_path1 = resource_path(relative_path=self.locale.i10n('police-car-mini'))
            police_poisk_path2 = resource_path(relative_path=self.locale.i10n('police-car-big'))
            police_poisk_path_list = [
                police_poisk_path1,
                police_poisk_path2
            ]
            # Проверяю в цикле кнопку ПОИСК т.к их может быть несколько
            while not self.task_manager.stop_event.is_set():
                for path in police_poisk_path_list:
                    if not self.task_manager.stop_event.is_set():
                        coord_police_poisk = find_template_matches(path, threshold=0.9)
                        if coord_police_poisk:
                            logger.info(msg="GAME OBJECT SERVICE: POLICE POISK - BUTTON POISK DETECTED")
                            self.clicker_manager.click(coord_police_poisk[0][0]+10, coord_police_poisk[0][1])
                            time.sleep(12)
                            police_poisk_ok_path = resource_path(relative_path=self.locale.i10n('police-ok'))
                            # Проверяю в цикле кнопку ОК т.к их может быть несколько
                            while not self.task_manager.stop_event.is_set():

                                coord_police_poisk_ok = find_template_matches_color(police_poisk_ok_path)
                                if coord_police_poisk_ok and not self.task_manager.stop_event.is_set():
                                    logger.info(msg="GAME OBJECT SERVICE: POLICE POISK - BUTTON OK DETECTED")
                                    self.clicker_manager.click(coord_police_poisk_ok[0][0], coord_police_poisk_ok[0][1])
                                    time.sleep(5)
                                else:
                                    logger.info(msg="GAME OBJECT SERVICE: POLICE POISK - BUTTON OK DONT DETECTED")
                                    time.sleep(1)
                                    break
                    else:
                        break
                else:
                    logger.info(msg="GAME OBJECT SERVICE: POLICE POISK - BUTTON POISK DONT DETECTED")
                    self.clicker_manager.press_ecs()
                    time.sleep(4)
                    break
        else:
            logger.info(msg="GAME OBJECT SERVICE: Police build don't detected")
            time.sleep(1)

    @check_stop_func
    def go_to_ally(self):
        self.go_to_shelter()
        path_alliance_btn = resource_path(relative_path="app\\img\\game_button\\ally\\alliance.png")
        coord_alliance = find_template_matches(path_alliance_btn)
        if coord_alliance and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY BTN FIND")
            self.clicker_manager.click(coord_alliance[0][0], coord_alliance[0][1])
            time.sleep(3)
        else:
            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY BTN UNDEFIND")

    @check_stop_func
    def go_to_company(self):
        self.go_to_shelter()
        path_company = resource_path(relative_path="app\\img\\game_button\\company\\company.png")
        coord_company = find_template_matches(path_company)
        if coord_company and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: COMPANY BTN FIND")
            self.clicker_manager.click(coord_company[0][0], coord_company[0][1])
            time.sleep(3)
        else:
            logger.info(msg="GAME OBJECT SERVICE: COMPANY BTN UNDEFIND")
            self.go_to_shelter()

    @check_stop_func
    def take_ally_technology_bonus(self, window):
        self.go_to_shelter()
        time.sleep(2)
        self.go_to_ally()
        time.sleep(3)
        path_alliance_thno = resource_path(relative_path="app\\img\\game_button\\ally\\alliance_tehnology.png")
        coord_alliance_thno = find_template_matches(path_alliance_thno)
        # Проверяю наличие кнопки технологии
        if coord_alliance_thno and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO BONUS BTN FIND")
            self.clicker_manager.click(coord_alliance_thno[0][0], coord_alliance_thno[0][1])
                # Жду когда помигаер рука таргета (она перекрывает нужную кнопку)
            time.sleep(8)
                # Ищу таргет
            path_alliance_thno_target = resource_path(relative_path=self.locale.i10n('alliance-techno-target'))
            coord_alliance_thno_target = find_template_matches(path_alliance_thno_target)
            if coord_alliance_thno_target and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: TARGET BTN FIND")
                self.clicker_manager.click(coord_alliance_thno_target[0][0], coord_alliance_thno_target[0][1])
                time.sleep(2)
                    # надо проверить есть ли кнопка Иследовать
                    # надо проверить есть ли кнопка Использовать
                while not self.task_manager.stop_event.is_set():
                        # надо проверить есть ли кнопка пожертвовать, если есть то начать цикл
                    path_alliance_thno_don = resource_path(relative_path=self.locale.i10n('alliance-techno-donate'))
                    coord_alliance_thno_don = find_template_matches(path_alliance_thno_don)
                    if coord_alliance_thno_don:
                        path_alliance_thno_count = resource_path(relative_path=self.locale.i10n('alliance-techno-donate-count'))
                        coord_alliance_thno_count = find_template_matches(path_alliance_thno_count, threshold=0.97)
                        if coord_alliance_thno_count and not self.task_manager.stop_event.is_set():
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: DONATE COUNT **NULL** ")
                            for i in range(10):
                                if not self.task_manager.stop_event.is_set():
                                    self.clicker_manager.proportion_click_in_window(window=window.window,target_x=990, target_y=610)
                                    time.sleep(0.5)
                            break
                        else:
                            #990 610
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: DONATE COUNT NOT NULL PROPORTIONAL CLICK TO DONATE")
                            if not self.task_manager.stop_event.is_set():
                                self.clicker_manager.proportion_click_in_window(window=window.window,target_x=990, target_y=610)
                                time.sleep(0.5)
                            else:
                                break
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO:DONETE UNDEFINDE")
                        break
                # ТУТ ВСЕ ВЫПОЛНЕНО.
                self.go_to_shelter()
                time.sleep(2)
                # Тут Таргет кнопка не найдена
            else:
                logger.warning(msg="GAME OBJECT SERVICE: ALLY TECHNO: TARGET BTN UNDEFINDED")
                self.go_to_shelter()
                time.sleep(2)
            # Тут Кнопка технологии не найдена
        else:
            logger.warning(msg="GAME OBJECT SERVICE: ALLY TECHNO BONUS BTN UNDEFINDED")
            self.go_to_shelter()
            time.sleep(1)

    @check_stop_func
    def take_alliance_bonus(self, window):

        logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY BONUS STARTED")
        path_alliance_btn = resource_path(relative_path="app\\img\\game_button\\ally\\alliance.png")
        coord_alliance = find_template_matches(path_alliance_btn)
        if coord_alliance and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY BTN FIND")
            self.clicker_manager.click(coord_alliance[0][0], coord_alliance[0][1])
            time.sleep(3)
            # Проверяю вступил ли в альянс
            path_alliance_join = resource_path(relative_path=self.locale.i10n('alliance-join'))
            coord_alliance_join = find_template_matches(path_alliance_join)
            if coord_alliance_join:
                self.go_to_shelter()
                return

            path_alliance_terry_btn = resource_path(relative_path="app\\img\\game_button\\ally\\alliance_terry.png")
            coord_alliance_terry = find_template_matches(path_alliance_terry_btn)

            if coord_alliance_terry and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TERRY BTN FIND")
                self.clicker_manager.click(coord_alliance_terry[0][0], coord_alliance_terry[0][1])
                time.sleep(3)

                path_alliance_terry_get_btn = resource_path(relative_path=self.locale.i10n('alliance-terry-get'))
                coord_alliance_terry_get = find_template_matches(path_alliance_terry_get_btn)

                if coord_alliance_terry_get and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TERRY BONUS GET")
                    self.clicker_manager.click(coord_alliance_terry_get[0][0], coord_alliance_terry_get[0][1])
                    time.sleep(3)
                    self.clicker_manager.press_ecs()
                    time.sleep(3)
                else:
                    logger.warning(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TERRY BONUS UNDEFINDED")
                    self.clicker_manager.press_ecs()
                    time.sleep(2)
            else:
                time.sleep(1)
                logger.warning(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TERRY BTN UNDEFINDED")
                self.go_to_ally()

            # =============== ВЗНОСЫ В ТЕХНОЛОГИИ ===================== #
            path_alliance_thno = resource_path(relative_path="app\\img\\game_button\\ally\\alliance_tehnology.png")
            coord_alliance_thno = find_template_matches(path_alliance_thno)
            # Проверяю наличие кнопки технологии
            if coord_alliance_thno and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO BONUS BTN FIND")
                self.clicker_manager.click(coord_alliance_thno[0][0], coord_alliance_thno[0][1])
                # Жду когда помигаер рука таргета (она перекрывает нужную кнопку)
                time.sleep(8)
                # Ищу таргет
                path_alliance_thno_target = resource_path(relative_path=self.locale.i10n('alliance-techno-target'))
                coord_alliance_thno_target = find_template_matches(path_alliance_thno_target)
                if coord_alliance_thno_target and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: TARGET BTN FIND")
                    self.clicker_manager.click(coord_alliance_thno_target[0][0], coord_alliance_thno_target[0][1])
                    time.sleep(2)
                    # надо проверить есть ли кнопка Иследовать
                    # надо проверить есть ли кнопка Использовать
                    while not self.task_manager.stop_event.is_set():
                        # надо проверить есть ли кнопка пожертвовать, если есть то начать цикл
                        path_alliance_thno_don = resource_path(relative_path=self.locale.i10n('alliance-techno-donate'))
                        coord_alliance_thno_don = find_template_matches(path_alliance_thno_don)
                        if coord_alliance_thno_don:
                            path_alliance_thno_count = resource_path(relative_path=self.locale.i10n('alliance-techno-donate-count'))
                            coord_alliance_thno_count = find_template_matches(path_alliance_thno_count, threshold=0.97)
                            if coord_alliance_thno_count and not self.task_manager.stop_event.is_set():
                                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: DONATE COUNT **NULL** ")
                                for i in range(10):
                                    if not self.task_manager.stop_event.is_set():
                                        self.clicker_manager.proportion_click_in_window(window=window.window,target_x=990, target_y=610)
                                        time.sleep(0.5)
                                break
                            else:
                                #990 610
                                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO: DONATE COUNT NOT NULL PROPORTIONAL CLICK TO DONATE")
                                if not self.task_manager.stop_event.is_set():
                                    self.clicker_manager.proportion_click_in_window(window=window.window,target_x=990, target_y=610)
                                    time.sleep(0.5)
                                else:
                                    break
                        else:
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY TECHNO:DONETE UNDEFINDE")
                            break
                    self.clicker_manager.press_ecs()
                    time.sleep(1)
                    self.clicker_manager.press_ecs()
                    time.sleep(1)
                # Тут Таргет кнопка не найдена
                else:
                    logger.warning(msg="GAME OBJECT SERVICE: ALLY TECHNO: TARGET BTN UNDEFINDED")
                    self.go_to_ally()
                    time.sleep(2)
            # Тут Кнопка технологии не найдена
            else:
                logger.warning(msg="GAME OBJECT SERVICE: ALLY TECHNO BONUS BTN UNDEFINDED")
                self.go_to_ally()
                time.sleep(1)


            # ========================== GIFT ====================================#
            path_alliance_gift = resource_path(relative_path="app\\img\\game_button\\ally\\alliance_gift.png")
            coord_alliance_gift = find_template_matches(path_alliance_gift)
            # Тут я проверяю кнопку Подарка
            if coord_alliance_gift and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT BTN FIND")
                self.clicker_manager.click(coord_alliance_gift[0][0], coord_alliance_gift[0][1])
                time.sleep(3)
                # Тут Перехожу в вкладку подарки за донат
                path_alliance_gift_buy = resource_path(relative_path=self.locale.i10n('alliance-gift-buy'))
                coord_alliance_gift_buy = find_template_matches(path_alliance_gift_buy)

                if coord_alliance_gift_buy and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT BUY BTN FIND")
                    self.clicker_manager.click(coord_alliance_gift_buy[0][0], coord_alliance_gift_buy[0][1])
                    time.sleep(3)

                    while not self.task_manager.stop_event.is_set():
                        # Ищу кнопку получать
                        path_alliance_gift_get = resource_path(relative_path=self.locale.i10n('alliance-gift-get'))
                        coord_alliance_gift_get = find_template_matches(path_alliance_gift_get, threshold=0.95)
                        if coord_alliance_gift_get:
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT BUY: GET BTN FIND")
                            self.clicker_manager.click(coord_alliance_gift_get[0][0], coord_alliance_gift_get[0][1])
                            time.sleep(1)
                        else:
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT BUY: GET BTN UNDEFIND")
                            break
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT BUY BTN UNDEFIND")
                    self.go_to_shelter()

                # Перехожу в вкладку подарки за активность
                path_alliance_gift_active = resource_path(relative_path=self.locale.i10n('alliance-gift-active'))
                coord_alliance_gift_active = find_template_matches(path_alliance_gift_active, threshold=0.7)
                if coord_alliance_gift_active and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT ACTIVE BTN FIND")
                    self.clicker_manager.click(coord_alliance_gift_active[0][0], coord_alliance_gift_active[0][1])
                    time.sleep(2)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT ACTIVE BTN FIND PROPOTIONAL")
                    self.clicker_manager.proportion_click_in_window(window=window.window, target_x=790,target_y=125)
                    time.sleep(1)
                    # Проверяю есть ли кнопка получить
                path_alliance_gift_get = resource_path(relative_path=self.locale.i10n('alliance-gift-get'))
                coord_alliance_gift_get = find_template_matches(path_alliance_gift_get, threshold=0.95)
                if coord_alliance_gift_get and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT ACTIVE: GET BTN FIND")
                    path_alliance_gift_get_all = resource_path(relative_path=self.locale.i10n('alliance-gift-get-all'))
                    coord_alliance_gift_get_all = find_template_matches(path_alliance_gift_get_all)
                        # Проверяю кнопку собрать все
                    if coord_alliance_gift_get_all:
                        logger.info(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT ACTIVE: GET ALL BTN FIND")
                        self.clicker_manager.click(coord_alliance_gift_get_all[0][0], coord_alliance_gift_get_all[0][1])
                        time.sleep(1)
                        self.go_to_shelter()
                    else:
                        logger.warning(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT ACTIVE: GET ALL BTN UNDEFIND")
                        self.go_to_shelter()

            else:
                logger.warning(msg="GAME OBJECT SERVICE: TAKE ALLY: ALLY GIFT: GIFT BTN UNDEFIND")
                self.go_to_shelter()
                time.sleep(1)

        else:
            self.go_to_shelter()

    @check_stop_func
    def take_mail(self, window):
        path_mail = resource_path(relative_path="app\\img\\game_button\\mail\\mail.png")
        path_get_bonus = resource_path(relative_path=self.locale.i10n('mail-get-bonus'))
        coord_mail = find_template_matches(path_mail)
        if coord_mail and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL: MAIL BTN FIND")
            self.clicker_manager.click(coord_mail[0][0], coord_mail[0][1])
            time.sleep(3)
            # 600 75 SYSTEM
            path_system1 = resource_path(relative_path=self.locale.i10n('mail-system1'))
            path_system2 = resource_path(relative_path=self.locale.i10n('mail-system2'))

            # GET
            path_mail_get = resource_path(relative_path=self.locale.i10n('mail-get'))
            coord_mail_get = find_template_matches(path_mail_get)
            if not coord_mail_get:
                logger.warning(msg="GAME OBJECT SERVICE: TAKE MAIL SYSTEM: MAIL BTN UNDEFIND")
                self.go_to_shelter()
                return

            path_sys = [
                path_system1,
                path_system2
            ]
            for path in path_sys:
                coord_sys = find_template_matches(path)
                if coord_sys and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL SYSTEM: SYSTEM BTN FIND")
                    self.clicker_manager.click(coord_sys[0][0], coord_sys[0][1])
                    time.sleep(1)
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL SYSTEM: GET BONUS")
                    self.clicker_manager.click(coord_mail_get[0][0], coord_mail_get[0][1])
                    time.sleep(3)
                    if find_template_matches(path_get_bonus):
                        self.clicker_manager.press_ecs()
                        time.sleep(3)
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL SYSTEM: SYS NO HAVE BONUS")

                    break


            # 440 75 ALLY
            path_mail_ally = resource_path(relative_path=self.locale.i10n('mail-ally'))
            coord_mail_ally = find_template_matches(path_mail_ally)
            if coord_mail_ally and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL ALLY: ALLY BTN FIND")
                self.clicker_manager.click(coord_mail_ally[0][0], coord_mail_ally[0][1])
                time.sleep(1)
                logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL ALLY: GET BONUS")
                self.clicker_manager.click(coord_mail_get[0][0], coord_mail_get[0][1])
                time.sleep(3)
                if find_template_matches(path_get_bonus):
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL ALLY: ESC TO GET BONUS")
                    self.clicker_manager.press_ecs()
                    time.sleep(3)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL ALLY: ALLY NO HAVE BONUS")

            else:
                self.go_to_shelter()
                return

            path_mail_logs = resource_path(relative_path=self.locale.i10n('mail-logs'))
            coord_mail_logs = find_template_matches(path_mail_logs)
            if coord_mail_logs and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL LOGS: LOGS BTN FIND")
                self.clicker_manager.click(coord_mail_logs[0][0], coord_mail_logs[0][1])
                time.sleep(1)
                logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL LOGS: GET BONUS")
                self.clicker_manager.click(coord_mail_get[0][0], coord_mail_get[0][1])
                time.sleep(3)
                if find_template_matches(path_get_bonus):
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL LOGS: ESC TO GET BONUS")
                    self.clicker_manager.press_ecs()
                    time.sleep(3)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MAIL LOGS: LOGS NO HAVE BONUS")
            else:
                self.go_to_shelter()
                return

            self.go_to_shelter()
            time.sleep(4)

    @check_stop_func
    def take_expedition(self, window):
        self.go_to_region()
        time.sleep(3)
        self.go_to_shelter()
        time.sleep(3)
        if not self.task_manager.stop_event.is_set():
            self.clicker_manager.moving_screen_to_baricades(window=window.window)
        time.sleep(4)

        path_expedition = resource_path(relative_path="app\\img\\game_button\\exspedition\\expedition.png")
        path_expedition2 = resource_path(relative_path="app\\img\\game_button\\exspedition\\expedition2.png")
        path_expedition3 = resource_path(relative_path="app\\img\\game_button\\exspedition\\expedition3.png")
        path_expedition4 = resource_path(relative_path="app\\img\\game_button\\exspedition\\expedition4.png")
        path_exp_gift = [
            path_expedition2,
            path_expedition3
        ]
        path_exp = [
            path_expedition,
            path_expedition4,
        ]

        coord_exp_gift = []
        coord_exp = []
        for i in range(5):
            if not self.task_manager.stop_event.is_set() and not coord_exp_gift:
                for path in path_exp_gift:
                    coord_exp_gift = find_template_matches(path, threshold=0.7)
                    if coord_exp_gift and not self.task_manager.stop_event.is_set():
                        break
                time.sleep(0.5)
            else:
                break
        for i in range(5):
            if not self.task_manager.stop_event.is_set() and not coord_exp:
                for path in path_exp:
                    coord_exp = find_template_matches(path, threshold=0.7)
                    if coord_exp and not self.task_manager.stop_event.is_set():
                        break
                time.sleep(0.5)
            else:
                break

        if coord_exp_gift and not self.task_manager.stop_event.is_set():
            coord = coord_exp_gift
            logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND EXPEDITION BTN")
            self.clicker_manager.click(coord[0][0], coord[0][1])
            time.sleep(3)
            path_expedition_get1 = resource_path(relative_path=self.locale.i10n('exp-get1'))
            coord_expedition_get1 = find_template_matches(path_expedition_get1)

            if coord_expedition_get1 and not self.task_manager.stop_event.is_set():
                self.clicker_manager.click(coord_expedition_get1[0][0], coord_expedition_get1[0][1])
                time.sleep(3)
                self.clicker_manager.press_ecs()
                time.sleep(3)

        elif coord_exp and not self.task_manager.stop_event.is_set():
            coord = coord_exp
            if coord and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND EXPEDITION BTN")
                self.clicker_manager.click(coord[0][0], coord[0][1])
                time.sleep(3)
                path_expedition_get3 = resource_path(relative_path=self.locale.i10n('exp-get3'))
                coord_expedition_get3 = find_template_matches(path_expedition_get3)

                if coord_expedition_get3 and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND GET#1 BTN")
                    self.clicker_manager.click(coord_expedition_get3[0][0], coord_expedition_get3[0][1])
                    time.sleep(2)
                    path_expedition_get2 = resource_path(relative_path=self.locale.i10n('exp-get2'))
                    coord_expedition_get2 = find_template_matches(path_expedition_get2)
                    if coord_expedition_get2 and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND GET#2 BTN")
                        self.clicker_manager.click(coord_expedition_get2[0][0], coord_expedition_get2[0][1])
                        time.sleep(3)
                    self.clicker_manager.press_ecs()
                    time.sleep(1.5)
                    self.clicker_manager.press_ecs()
                    time.sleep(1.5)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND GET#1 BTN UNDEFIND")
                    self.clicker_manager.press_ecs()
                    time.sleep(1.5)
        else:
            logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: EXPEDITION BTN UNDEFINDED")
            self.go_to_region()
            time.sleep(3)
            self.go_to_shelter()
            time.sleep(3)
            if not self.task_manager.stop_event.is_set():
                self.clicker_manager.moving_screen_to_baricades(window=window.window)
            time.sleep(4)

        logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: PPL SAVE STARTED")

        while not self.task_manager.stop_event.is_set():
            path_ppl_help = resource_path(relative_path="app\\img\\game_button\\exspedition\\ppl_help.png")
            path_ppl_help2 = resource_path(relative_path="app\\img\\game_button\\exspedition\\ppl_help2.png")
            path_list_ppl = [
                path_ppl_help,
                path_ppl_help2
            ]
            for i in range(5):
                if not self.task_manager.stop_event.is_set():
                    for path in path_list_ppl:
                        coord_ppl = find_template_matches(path, threshold=0.7)
                        if coord_ppl and not self.task_manager.stop_event.is_set():
                            break
                    time.sleep(0.5)
                else:
                    break

            if coord_ppl and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: FIND PPL")
                self.clicker_manager.click(coord_ppl[0][0], coord_ppl[0][1])
                time.sleep(3)

                path_ppl_help = resource_path(relative_path=self.locale.i10n('exp-ppl-help-get'))
                coord_ppl_help = find_template_matches(path_ppl_help)
                if coord_ppl_help and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: GET PPL")
                    self.clicker_manager.click(coord_ppl_help[0][0], coord_ppl_help[0][1])
                    time.sleep(3)
            else:
                logger.info(msg="GAME OBJECT SERVICE: TAKE EXPEDITION: PPL BTN UNDEFIND")
                break

        self.go_to_after_shift()
        time.sleep(2)

    @check_stop_func
    def take_compamy(self, window, task_arena = None):
        path_company = resource_path(relative_path="app\\img\\game_button\\company\\company.png")
        coord_company = find_template_matches(path_company)
        logger.info(msg="GAME OBJECT SERVICE: TAKE COMPANY: STARTED")
        if coord_company and not self.task_manager.stop_event.is_set():
            self.clicker_manager.click(coord_company[0][0], coord_company[0][1])
            time.sleep(3)

            # ============= MEMYARY =================
            logger.info(msg="GAME OBJECT SERVICE: TAKE MEMORY: STARTED")
            path_memyary = resource_path(relative_path=self.locale.i10n('company-memyary'))
            coord_memyary = find_template_matches(path_memyary)
            if coord_memyary and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE MEMORY: MEMORY BTN FIND")
                self.clicker_manager.click(coord_memyary[0][0], coord_memyary[0][1])
                time.sleep(3)
                path_memyary_chest = resource_path(relative_path="app\\img\\game_button\\company\\memyary_chest.png")
                coord_memyary_chest = find_template_matches(path_memyary_chest)
                if coord_memyary_chest and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MEMORY: CHEST BTN FIND")
                    self.clicker_manager.click(coord_memyary_chest[0][0], coord_memyary_chest[0][1])
                    time.sleep(3)
                    self.clicker_manager.press_ecs()
                    time.sleep(2)
                    self.clicker_manager.press_ecs()
                    time.sleep(1)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE MEMORY: FAIL CHEST BTN UNDEFIND")
                    self.clicker_manager.press_ecs()
                    time.sleep(3)
            else:
                logger.info(msg="GAME OBJECT SERVICE: TAKE MEMORY: FAIL MEMORY BTN UNDEFIND")
                self.go_to_ally()
            # ============= ARENA =================

            logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: STARTED")
            path_arena = resource_path(relative_path=self.locale.i10n('company-arena'))
            coord_arena = find_template_matches(path_arena)
            # Переходим в Арена
            if coord_arena and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: FIND ARENA BTN")
                self.clicker_manager.click(coord_arena[0][0], coord_arena[0][1])
                time.sleep(5)
                # Проверяем всплывающее окна то что сменился ранг
                path_arena_rank = resource_path(relative_path=self.locale.i10n('company-arena-get-rank'))
                coord_arena_rank = find_template_matches(path_arena_rank)
                logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: CHECK RANK WINDOW")
                if coord_arena_rank and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: GET RANK WINDOW")
                    self.clicker_manager.click(coord_arena_rank[0][0], coord_arena_rank[0][1])
                    time.sleep(3)
                # Проверяем то что сундук заполнен
                path_arena_chest = resource_path(relative_path="app\\img\\game_button\\company\\arena_chest.png")
                coord_arena_chest = find_template_matches(path_arena_chest)
                if coord_arena_chest and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: GET CHEST")
                    self.clicker_manager.click(coord_arena_chest[0][0], coord_arena_chest[0][1])
                    time.sleep(3)
                    path_arena_chest_get = resource_path(relative_path=self.locale.i10n('company-arena-get-chest'))
                    coord_arena_chest_get = find_template_matches(path_arena_chest_get)
                    if coord_arena_chest_get and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: GET ARENA PRIZE")
                        self.clicker_manager.click(coord_arena_chest_get[0][0], coord_arena_chest_get[0][1])
                        time.sleep(3)
                    else:
                        self.clicker_manager.press_ecs()
                        time.sleep(3)

                else:
                    logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: CHEST[EMPTY] - NOT FIND.")
                if task_arena == True:
                    arena_trigger = True
                else:
                    arena_trigger = False
                if arena_trigger and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: TAKE ARENA: ARENA BATTLE TRIGGER IS TRUE")
                    count_arena = 0
                    count_fail_arena = 0
                    while not self.task_manager.stop_event.is_set():
                        if count_arena == 5:
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: COUNT ARENA TASK END")
                            break

                        if count_fail_arena == 3:
                            logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: COUNT FAIL TASK END")
                            break

                        time.sleep(2)
                        logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: GET BATTLE TASK")
                        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1040, target_y=690)
                        time.sleep(6)
                        # Проверяю есть ли ходы
                        path_buy = resource_path(relative_path=self.locale.i10n('company-arena-buy-game'))
                        coord_buy = find_template_matches(path_buy)
                        if coord_buy:
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: END BATTLE COUNT")
                            time.sleep(1)
                            self.clicker_manager.press_ecs()
                            break
                        time.sleep(4)
                        path_check_fully = resource_path(relative_path="app\\img\\game_button\\company\\arena_check_fully.png")
                        coord_check_fully = find_template_simple(path_check_fully)
                        # Проверяю стоит ли чекбокс пропустить битву
                        if coord_check_fully and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: CHECKBOX IS TRUE")
                            time.sleep(2)
                        # Чекбокс не стоит
                        else:
                            # Ищу пустой чекбокс пропустить битву
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: CHECKBOX IS FALSE")
                            path_check_empty = resource_path(relative_path="app\\img\\game_button\\company\\arena_check_empty.png")
                            coord_check_empty = find_template_simple(path_check_empty, threshold=0.9)
                            if coord_check_empty and not self.task_manager.stop_event.is_set():
                                logger.info("GAME OBJECT SERVICE: TAKE ARENA: CLICK CHECKBOX TO TRUE")
                                self.clicker_manager.click(coord_check_empty[0][0], coord_check_empty[0][1])
                                time.sleep(4)

                        path_start_battle = resource_path(relative_path=self.locale.i10n('company-arena-start-battle'))
                        coord_start_battle = find_template_matches(path_start_battle)
                        if coord_start_battle and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: START BATTLE")
                            self.clicker_manager.click(coord_start_battle[0][0], coord_start_battle[0][1])
                            count_arena += 1
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: COUNT BATTLE TASK UP TO:%s", count_arena)
                            time.sleep(10)
                            # Проверить не появился ли ранк 640 600
                            path_uprank = resource_path(relative_path=self.locale.i10n('company-arena-get-rank-battle'))
                            coord_uprank= find_template_matches(path_uprank)
                            if coord_uprank:
                                logger.info("GAME OBJECT SERVICE: TAKE ARENA: RANK IS UP")
                                self.clicker_manager.click(coord_uprank[0][0], coord_uprank[0][1])
                                time.sleep(3)

                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: END BATTLE. PROPORTIONAL CLICK")
                            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=620, target_y=640)
                            time.sleep(4)
                        else:
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: START BATTLE BTN UNDEFIND")
                            count_fail_arena += 1
                            logger.info("GAME OBJECT SERVICE: TAKE ARENA: COUNT FAIL TASK UP TO:%s", count_fail_arena)
                            # Не нашел кнопку начать битву
                            self.go_to_company()
                            time.sleep(2)
                            path_arena = resource_path(relative_path=self.locale.i10n('company-arena'))
                            coord_arena = find_template_matches(path_arena)
                            # Переходим в Арена
                            if coord_arena and not self.task_manager.stop_event.is_set():
                                logger.info(msg="GAME OBJECT SERVICE: TAKE ARENA: FIND ARENA BTN")
                                self.clicker_manager.click(coord_arena[0][0], coord_arena[0][1])
                                time.sleep(5)

                # Выход из арена меню
                logger.info("GAME OBJECT SERVICE: TAKE ARENA: ARENA EXIT")
                self.clicker_manager.press_ecs()

                time.sleep(3)
            # ============= HUNT =================
            logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: STARTED")
            path_hunt = resource_path(relative_path="app\\img\\game_button\\company\\hunt.png")
            path_hunt2 = resource_path(relative_path="app\\img\\game_button\\company\\hunt.png")
            path_hunt_list = [
                path_hunt,
                path_hunt2
            ]
            for path in path_hunt_list:
                coord_hunt = find_template_matches(path)
                if coord_hunt:
                    break

            if coord_hunt and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: HUNT BTN FIND")
                self.clicker_manager.click(coord_hunt[0][0], coord_hunt[0][1])
                time.sleep(3)
                path_hunt_roulet = resource_path(relative_path="app\\img\\game_button\\company\\hunt_roulet.png")
                coord_hunt_roulet = find_template_matches(path_hunt_roulet)
                if coord_hunt_roulet and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: ROULET BTN FIND")
                    self.clicker_manager.click(coord_hunt_roulet[0][0], coord_hunt_roulet[0][1])
                    time.sleep(3)
                    path_hunt_gift = resource_path(relative_path="app\\img\\game_button\\company\\hunt_gift.png")
                    coord_hunt_gift = find_template_matches(path_hunt_gift)
                    if coord_hunt_gift and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: GIFT BTN FIND")
                        self.clicker_manager.click(coord_hunt_gift[0][0], coord_hunt_gift[0][1])
                        time.sleep(3)
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: HUNT BTN FIND PROPORTIONAL")
                        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1190, target_y=640)
                        time.sleep(3)
                    path_hunt_fail_gift = resource_path(relative_path=self.locale.i10n('company-hunt-fail-gift'))
                    coord_hunt_fail_gift = find_template_matches(path_hunt_fail_gift)
                    if coord_hunt_fail_gift and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: FAIL GET GIFT - TODAY USED")
                        self.clicker_manager.press_ecs()
                        time.sleep(3)

                    path_hunt_role = resource_path(relative_path="app\\img\\game_button\\company\\hunt_role.png")
                    coord_hunt_role = find_template_matches(path_hunt_role)
                    if coord_hunt_role and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: ROLE PRIZE")
                        self.clicker_manager.click(coord_hunt_role[0][0], coord_hunt_role[0][1])
                        time.sleep(6)
                        self.go_to_shelter()
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: ROLE PRIZE PROPORTIONAL")
                        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=130, target_y=630)
                        time.sleep(6)
                        self.go_to_shelter()
            else:
                logger.info(msg="GAME OBJECT SERVICE: TAKE HUNT: FAIL HUNT BTN UNDEFINDFIND")
                self.go_to_shelter()

    @check_stop_func
    def take_cex(self, window):
        cex_path = resource_path(relative_path="app\\img\\game_button\\cex.png")
        cex_path2 = resource_path(relative_path="app\\img\\game_button\\cex2.png")
        cex_path_list = [
            cex_path, cex_path2
        ]
        coord_cex = []
        for i in range(5):
            if coord_cex:
                break
            else:
                for path in cex_path_list:
                    cex = find_template_matches(path)
                    if cex:
                        coord_cex.extend(cex)
                        break
                    time.sleep(0.6)
        if coord_cex and not self.task_manager.stop_event.is_set():
            try:
                logger.info(msg="GAME OBJECT SERVICE: CEX IN SCREEN")
                self.clicker_manager.click(coord_cex[0][0], coord_cex[0][1])
                time.sleep(3)
                logger.info(msg="GAME OBJECT SERVICE: CEX GATHER")
                # Нажатие МОЖНО СОБРАТЬ
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=980, target_y=195)
                time.sleep(5)
                # Нажатие пустое место для сбора
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=580, target_y=700)
                time.sleep(2)
                while not self.task_manager.stop_event.is_set():
                    cex_build = resource_path(relative_path=self.locale.i10n('cex-build'))
                    cex_b = find_template_matches_color(cex_build)
                    if cex_b and not self.task_manager.stop_event.is_set():
                        logger.info(msg="GAME OBJECT SERVICE: CEX BUILD BUTTON IS ACTIVE")
                        self.clicker_manager.click(cex_b[0][0], cex_b[0][1])
                        time.sleep(3.5)
                        cex_b = []
                        continue
                    else:
                        logger.info(msg="GAME OBJECT SERVICE: CEX BUILD BUTTON IS NOT ACTIVE")
                        time.sleep(1)
                        break

                self.go_to_shelter()

            except IndexError as error:
                pass
        else:
            logger.info(msg="GAME OBJECT SERVICE: CEX NOT DEFIENED")

    @check_stop_func
    def take_ferm(self):

        food_ferm_path1 = resource_path(relative_path="app\\img\\game_button\\food_ferm.png")
        food_ferm_path2 = resource_path(relative_path="app\\img\\game_button\\food_ferm2.png")
        food_ferm_path3 = resource_path(relative_path="app\\img\\game_button\\food_ferm3.png")
        food_ferm_path4 = resource_path(relative_path="app\\img\\game_button\\food_ferm4.png")
        food_ferm_list = [
            food_ferm_path1,
            food_ferm_path2,
            food_ferm_path3,
            food_ferm_path4
        ]
        for path in food_ferm_list:
            coord_food_ferm = find_template_matches(path)
            if coord_food_ferm and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: CLICK FOOD FERM")
                self.clicker_manager.click(coord_food_ferm[0][0], coord_food_ferm[0][1])
                break

        else:
            logger.info(msg="GAME OBJECT SERVICE: FERM NOT DEFIENED")

    @check_stop_func
    def take_racia(self):
        logger.info(msg="GAME OBJECT SERVICE: DAILY: RACIA SPACENIA START")
        path_racia = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\racia-spacenia.png")
        path_racia2 = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\racia-spacenia2.png")
        path_racia_list=[
            path_racia,
            path_racia2
        ]
        coord_racia = []
        for i in range(7):
            for path in path_racia_list:
                coord_racia = find_template_matches(path, threshold=0.7)
                if coord_racia:
                    break
            if coord_racia and not self.task_manager.stop_event.is_set():
                break
            else:
                time.sleep(0.5)
        if coord_racia and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: DAILY: CLICK RACIA SPACENIA")
            self.clicker_manager.click(coord_racia[0][0], coord_racia[0][1])
            time.sleep(3)
            path_get_free = resource_path(relative_path=self.locale.i10n('racia-get'))
            coord_get = find_template_matches(path_get_free)
            if coord_get:
                logger.info(msg="GAME OBJECT SERVICE: DAILY: CLICK SPASTI")
                self.clicker_manager.click(coord_get[0][0], coord_get[0][1])
                time.sleep(2)
                self.clicker_manager.press_ecs()
                time.sleep(2)
                self.clicker_manager.press_ecs()

            else:
                logger.info(msg="GAME OBJECT SERVICE: DAILY: FREE UNDEFIND")
                self.go_to_shelter()
                return

        else:
            logger.info(msg="GAME OBJECT SERVICE: DAILY: RACIA UNDEFIND")

    @check_stop_func
    def take_daily_bonus(self, window):
        logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: GET DAILY-MISSION BONUS START")
        path_daily = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\daily-btn.png")
        path_daily2 = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\daily-btn2.png")
        path_daily_list = [
            path_daily,
            path_daily2
        ]
        coord_daily = []
        for path in path_daily_list:
            coord_daily = find_template_matches(path)
            if coord_daily:
                break
        if coord_daily and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: FIND DAIY MISSION BTN")
            self.clicker_manager.click(coord_daily[0][0], coord_daily[0][1])
            time.sleep(3)
            path_daily_get = resource_path(relative_path=self.locale.i10n('daily-get'))
            coord_get = find_template_matches(path_daily_get)
            while not self.task_manager.stop_event.is_set():
                coord_get = find_template_matches(path_daily_get)
                if coord_get and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: FIND GET BTN")
                    self.clicker_manager.click(coord_get[0][0], coord_get[0][1])
                    time.sleep(2)
                else:
                    break

            path_daily_mission = resource_path(relative_path=self.locale.i10n('daily-mission1'))
            path_daily_mission2 = resource_path(relative_path=self.locale.i10n('daily-mission2'))
            path_list_daily_mission = [
                path_daily_mission,
                path_daily_mission2
            ]
            for path in path_list_daily_mission:
                coord_daily_mission = find_template_matches(path)
                if coord_daily_mission:
                    break

            if coord_daily_mission and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: FIND DAILY MISSION BTN")
                self.clicker_manager.click(coord_daily_mission[0][0], coord_daily_mission[0][1])
                time.sleep(2)
                coord_daily_get = find_template_matches(path_daily_get)
                if coord_daily_get and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: FIND GET BTN")
                    self.clicker_manager.click(coord_daily_get[0][0], coord_daily_get[0][1])
                    time.sleep(12)
                else:
                    logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: GET BTN UNDEFIND")

                chests = {
                        "app\\windows\\shelter\\daily\\img\\daily-20.png": (535,235),
                        "app\\windows\\shelter\\daily\\img\\daily-40.png": (695,235),
                        "app\\windows\\shelter\\daily\\img\\daily-60.png": (855,235),
                        "app\\windows\\shelter\\daily\\img\\daily-80.png": (1005,235),
                        "app\\windows\\shelter\\daily\\img\\daily-100.png": (1165,235),
                    }

                for path, coor in chests.items():
                    if self.task_manager.stop_event.is_set():
                        break
                    path_img = resource_path(relative_path=path)
                    coord_img = find_template_matches(path_img, threshold=0.95)
                    if coord_img and not self.task_manager.stop_event.is_set():
                        time.sleep(1)
                        continue
                    else:
                        self.clicker_manager.proportion_click_in_window(window=window.window,target_x=coor[0], target_y=coor[1])
                        time.sleep(10)
                        path_get_prize = resource_path(relative_path=self.locale.i10n('daily-get-prize'))
                        coord_get_prize = find_template_matches(path_get_prize)
                        if coord_get_prize and not self.task_manager.stop_event.is_set():
                            logger.info(msg="GAME OBJECT SERVICE: DAILY-MISSION: GET PRIZE BTN")
                            self.clicker_manager.click(coord_get_prize[0][0], coord_get_prize[0][1])
                            time.sleep(3)
                            break
                self.go_to_shelter()
            else:
                logger.info(msg="GAME OBJECT SERVICE: DAILY: DAILY MISSION BTN UNDEFIND")
                self.go_to_shelter()
        else:
            logger.info(msg="GAME OBJECT SERVICE: DAILY: DAILY-MISSION BONUS BTN UNDEFIND")

    @check_stop_func
    def take_shop(self):
        logger.info(msg="GAME OBJECT SERVICE:  GET SHOP START")
        path_shop = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\shop\\shop.png")
        path_shop2 = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\shop\\shop2.png")
        path_daily_list = [
            path_shop,
            path_shop2
        ]
        coord_shop = []
        # Ищу иконку магазина
        for _ in range (7):
            for path in path_daily_list:
                coord_shop = find_template_matches(path, threshold=0.7)
                if coord_shop:
                    break
            if coord_shop:
                    break
            time.sleep(0.4)
        if coord_shop and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: SHOP: FIND SHOP BTN")
            self.clicker_manager.click(coord_shop[0][0], coord_shop[0][1])
            time.sleep(2)

            path_celler_active = resource_path(relative_path=self.locale.i10n('take-shop-celler-active'))
            path_celler_inactive = resource_path(relative_path=self.locale.i10n('take-shop-celler-inactive'))

            path_celler =[
                path_celler_active,
                path_celler_inactive
            ]
            # Перехожу в вкладку продавца
            coord_celler = []
            for path in path_celler:
                coord_celler = find_template_matches(path)
                if coord_celler:
                    break
            if coord_celler and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: SHOP: FIND CELLER BTN")
                self.clicker_manager.click(coord_celler[0][0], coord_celler[0][1])
                time.sleep(2)

                path_box =  resource_path(relative_path="app\\windows\\shelter\\daily\\img\\shop\\box.png")
                coord_box = find_template_matches(path_box)
                if coord_box:
                    logger.info(msg="GAME OBJECT SERVICE: SHOP: CELLER OUT")
                    return
                path_food = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\shop\\shop-food.png")
                path_wood = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\shop\\shop-wood.png")

                path_buy_list =[
                    path_food,
                    path_wood
                ]
                down_screen = 0
                update_shop = False
                scroll_target = -75

                while not self.task_manager.stop_event.is_set():
                    if (down_screen > 9 and update_shop) or down_screen > 14:
                        logger.info(msg="GAME OBJECT SERVICE: SHOP: END")
                        break
                    else:
                        if down_screen > 9:
                            path_update = resource_path(relative_path=self.locale.i10n('take-shop-free-update'))
                            coord_update_btn = find_template_matches(path_update)
                            if coord_update_btn and not self.task_manager.stop_event.is_set():
                                logger.info(msg="GAME OBJECT SERVICE: SHOP: FIND FREE-UPDATE BTN")
                                self.clicker_manager.click(coord_update_btn[0][0], coord_update_btn[0][1])
                                update_shop = True
                                down_screen = 0
                                scroll_target = 75
                                time.sleep(2)
                    coord_buy = []
                    for path in path_buy_list:
                        coord = find_template_matches(path)
                        if coord:
                            coord_buy.extend(filter_coordinates(coords=coord, threshold=10))
                    if coord_buy and not self.task_manager.stop_event.is_set():
                        for x, y in coord_buy:
                            self.clicker_manager.click(x, y)
                            time.sleep(1)
                    else:
                        self.clicker_manager.scroll(target=scroll_target)
                        down_screen += 1
                self.go_to_shelter()
            else:
                logger.info(msg="GAME OBJECT SERVICE: SHOP: CELLER BTN UNDEFIND")
                self.go_to_shelter()
                time.sleep(3)
        else:
            logger.info(msg="GAME OBJECT SERVICE: SHOP: SHOP BTN UNDEFIND")


    def go_to_special_action(self):
        self.go_to_shelter()
        time.sleep(3)
        path_sa = resource_path(relative_path=self.locale.i10n('sa-icon1'))
        path_sa2 = resource_path(relative_path=self.locale.i10n('sa-icon2'))
        path_sa2 = resource_path(relative_path=self.locale.i10n('sa-icon3'))
        path_sa_list = [
            path_sa,
            path_sa2
        ]
        coord_sa = []
        while not self.task_manager.stop_event.is_set():
            for path in path_sa_list:
                coord_sa = find_template_matches(path)
                if coord_sa:
                    break
            # Входим в основное меню Специальных акций
            if coord_sa and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA BTN FIND")
                self.clicker_manager.click(coord_sa[0][0], coord_sa[0][1])
                time.sleep(3)
                break
            else:
                self.go_to_shelter()
                logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA BTN UNDEFIND")
                break

    @check_stop_func
    def take_special_action(self, window):

        self.go_to_special_action()
        SNAR_STATUS = False
        DETAL_STATUS = False
        MONTAJ_STATUS = False
        TRANSPORT_STATUS = False
        MEGA_STATUS = False

        check_times = 0
        while not self.task_manager.stop_event.is_set():
            if check_times > 5:
                break

            if SNAR_STATUS and DETAL_STATUS and MEGA_STATUS and TRANSPORT_STATUS and MONTAJ_STATUS:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: ALL MISSION GET")
                self.go_to_shelter()
                break
            if not SNAR_STATUS:
                SNAR_STATUS = self.take_sa_snar(window)
                time.sleep(1)
            if not DETAL_STATUS:
                DETAL_STATUS = self.take_sa_detal(window)
                time.sleep(1)
            if not MONTAJ_STATUS:
                MONTAJ_STATUS = self.take_sa_montaj(window)
                time.sleep(1)
            if not TRANSPORT_STATUS:
                TRANSPORT_STATUS = self.take_sa_transport(window)
                time.sleep(1)
            if not MEGA_STATUS:
                MEGA_STATUS = self.take_sa_mega(window)
                time.sleep(1)


            check_times += 1
        self.go_to_shelter()

    def take_sa_snar(self, window):
        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE START FUNC")
        # Ищем кнопку конкурс снаряжения
        path_sa_snar = resource_path(relative_path=self.locale.i10n('sa-snar-icon'))
        path_sa_snar_list = [
            path_sa_snar
        ]
        coord_sa_snar = []
        scroll_times = 0
        while not self.task_manager.stop_event.is_set():
            if scroll_times > 5:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE TASK UNDEFIND")
                return True
            for path in path_sa_snar_list:
                coord_sa_snar = find_template_matches(path)
                if coord_sa_snar:
                    break
            if coord_sa_snar:
                break
            else:
                self.clicker_manager.proportion_move_cursor_in_window(target_x=75, target_y=390, window=window.window)
                time.sleep(1)
                self.clicker_manager.scroll(target=-75)
                scroll_times += 1

        if coord_sa_snar and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE BTN FIND")
            self.clicker_manager.click(coord_sa_snar[0][0], coord_sa_snar[0][1])
            time.sleep(2)
            path_sa_snar_daily = resource_path(relative_path=self.locale.i10n('sa-snar-daily'))
            path_sa_snar_konkurs = resource_path(relative_path=self.locale.i10n('sa-snar-konkurs'))
            path_sa_snar_get = resource_path(relative_path=self.locale.i10n('sa-snar-get'))
            path_sa_snar_get_all = resource_path(relative_path=self.locale.i10n('sa-snar-get-all'))
            path_sa_snar_get_continue = resource_path(relative_path=self.locale.i10n('sa-snar-get-continue'))
            path_sa_snar_end_gift = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-end-gift.png")


            path_sa_snar_daily_list = [
                    path_sa_snar_daily
                ]
            path_sa_snar_konkurs_list = [
                    path_sa_snar_konkurs
                ]

            path_sa_snar_get_list = [
                    path_sa_snar_get
                ]
            path_sa_snar_get_all_list = [
                    path_sa_snar_get_all
                ]
            path_sa_snar_get_continue = [
                    path_sa_snar_get_continue
                ]

            coord_sa_snar_konkurs = []
            coord_sa_snar_daily = []
            coord_sa_snar_get = []
            coord_sa_snar_get_all = []
            coord_sa_snar_get_continue = []

            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE GET ALL TASK STARTED")
            for path in path_sa_snar_daily_list:
                coord_sa_snar_daily = find_template_matches(path)
                if coord_sa_snar_daily:
                    break
            if coord_sa_snar_daily and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-DAILY BTN FIND")
                self.clicker_manager.click(coord_sa_snar_daily[0][0], coord_sa_snar_daily[0][1])
                time.sleep(2)
                for path in path_sa_snar_get_list:
                    coord_sa_snar_get = find_template_matches(path)
                    if coord_sa_snar_get:
                        break
                if coord_sa_snar_get and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET BTN FIND")
                    coord_filter_snar_get = filter_coordinates(coords=coord_sa_snar_get, threshold=10)
                    for x,y in coord_filter_snar_get:
                        self.clicker_manager.click(x=x, y=y)
                        time.sleep(10)
                        path_sa_snar_get_exp_prize = resource_path(relative_path=self.locale.i10n('sa-snar-get_exp_prize'))
                        coord_sa_snar_get_exp_prize = find_template_matches(path_sa_snar_get_exp_prize)
                        if coord_sa_snar_get_exp_prize and not self.task_manager.stop_event.is_set():
                            time.sleep(1)
                            self.clicker_manager.click(coord_sa_snar_get_exp_prize[0][0], coord_sa_snar_get_exp_prize[0][1])
                            time.sleep(2)
                            break
                        else:
                            time.sleep(2)
                            break

            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE GET ALL TASK ENDED")
            # Конкурс снаряжения проверяю выполненые задания в основном бонусном меню
            for path in path_sa_snar_konkurs_list:
                coord_sa_snar_konkurs = find_template_matches(path)
                if coord_sa_snar_konkurs:
                    break
            if coord_sa_snar_konkurs and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-KONKURS BTN FIND")
                self.clicker_manager.click(coord_sa_snar_konkurs[0][0], coord_sa_snar_konkurs[0][1])
                time.sleep(2)
                for path in path_sa_snar_get_all_list:
                    coord_sa_snar_get_all = find_template_matches(path)
                    if coord_sa_snar_get_all:
                        break
                if coord_sa_snar_get_all and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET-ALL BTN FIND")
                    self.clicker_manager.click(coord_sa_snar_get_all[0][0], coord_sa_snar_get_all[0][1])
                    time.sleep(4)
                    self.clicker_manager.press_ecs()
                    time.sleep(1)
                    return True
                else:
                    for path in path_sa_snar_get_continue:
                        coord_sa_snar_get_continue = find_template_matches(path)
                        if coord_sa_snar_get_continue:
                            break
                    if coord_sa_snar_get_continue:
                        coord_end_gift = find_template_matches(path_sa_snar_end_gift)
                        if coord_end_gift and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET-LEG GIFT")
                            self.clicker_manager.click(coord_end_gift[0][0], coord_end_gift[0][1])
                            time.sleep(3)
                        else:
                            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET-PROPORTION-LEG GIFT")
                            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1185, target_y=445)
                            time.sleep(3)
                        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET-CONTINUE BTN FIND")
                        return True
                    else:
                        logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-GET-ALL OR CONINUE BTN UNDEFIND")
                        return False
            else:
                logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE-KONKURS BTN UNDEFIND")
                return False
        else:
            logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-SNARIAJENIE BTN UNDEFIND")
            return False

    def take_sa_detal(self, window):
        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL START FUNC")
        # Ищем кнопку конкурс снаряжения
        path_sa_detal = resource_path(relative_path=self.locale.i10n('sa-detal-icon'))
        path_sa_detal_list = [
            path_sa_detal
        ]
        coord_sa_detal = []
        scroll_times = 0
        while not self.task_manager.stop_event.is_set():
            if scroll_times > 5:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL TASK UNDEFIND")
                return True
            for path in path_sa_detal_list:
                coord_sa_detal = find_template_matches(path)
                if coord_sa_detal:
                    break
            if coord_sa_detal:
                break
            else:
                self.clicker_manager.proportion_move_cursor_in_window(target_x=75, target_y=390, window=window.window)
                time.sleep(1)
                self.clicker_manager.scroll(target=-75)
                scroll_times += 1

        if coord_sa_detal and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL BTN FIND")
            self.clicker_manager.click(coord_sa_detal[0][0], coord_sa_detal[0][1])
            time.sleep(2)
            path_sa_detal_daily = resource_path(relative_path=self.locale.i10n('sa-snar-daily'))
            path_sa_detal_konkurs = resource_path(relative_path=self.locale.i10n('sa-detal-konkurs'))
            path_sa_detal_get = resource_path(relative_path=self.locale.i10n('sa-snar-get'))
            path_sa_detal_get_all = resource_path(relative_path=self.locale.i10n('sa-snar-get-all'))
            path_sa_detal_get_continue = resource_path(relative_path=self.locale.i10n('sa-snar-get-continue'))
            path_sa_detal_end_gift = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-end-gift.png")

            path_sa_detal_daily_list = [
                    path_sa_detal_daily
                ]
            path_sa_detal_konkurs_list = [
                    path_sa_detal_konkurs
                ]
            path_sa_detal_get_list = [
                    path_sa_detal_get
                ]
            path_sa_detal_get_all_list = [
                    path_sa_detal_get_all
                ]
            path_sa_detal_get_continue = [
                    path_sa_detal_get_continue
                ]
            coord_sa_detal_konkurs = []
            coord_sa_detal_daily = []
            coord_sa_detal_get = []
            coord_sa_detal_get_all = []
            coord_sa_detal_get_continue = []


            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL GET ALL TASK STARTED")

            for path in path_sa_detal_daily_list:
                coord_sa_detal_daily = find_template_matches(path)
                if coord_sa_detal_daily:
                    break
            if coord_sa_detal_daily and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-DAILY BTN FIND")
                self.clicker_manager.click(coord_sa_detal_daily[0][0], coord_sa_detal_daily[0][1])
                time.sleep(2)
                for path in path_sa_detal_get_list:
                    coord_sa_detal_get = find_template_matches(path)
                    if coord_sa_detal_get:
                        break
                if coord_sa_detal_get and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET BTN FIND")
                    coord_filter_detal_get = filter_coordinates(coords=coord_sa_detal_get, threshold=10)
                    for x,y in coord_filter_detal_get:
                        self.clicker_manager.click(x=x, y=y)
                        time.sleep(10)
                        path_sa_snar_get_exp_prize = resource_path(relative_path=self.locale.i10n('sa-snar-get_exp_prize'))
                        coord_sa_snar_get_exp_prize = find_template_matches(path_sa_snar_get_exp_prize)
                        if coord_sa_snar_get_exp_prize and not self.task_manager.stop_event.is_set():
                            time.sleep(1)
                            self.clicker_manager.click(coord_sa_snar_get_exp_prize[0][0], coord_sa_snar_get_exp_prize[0][1])
                            time.sleep(2)
                            break
                        else:
                            time.sleep(2)
                            break


            for path in path_sa_detal_konkurs_list:
                coord_sa_detal_konkurs = find_template_matches(path)
                if coord_sa_detal_konkurs:
                    break
            if coord_sa_detal_konkurs and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-KONKURS BTN FIND")
                self.clicker_manager.click(coord_sa_detal_konkurs[0][0], coord_sa_detal_konkurs[0][1])
                time.sleep(2)
                for path in path_sa_detal_get_all_list:
                    coord_sa_detal_get_all = find_template_matches(path)
                    if coord_sa_detal_get_all:
                        break
                if coord_sa_detal_get_all and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET-ALL BTN FIND")
                    self.clicker_manager.click(coord_sa_detal_get_all[0][0], coord_sa_detal_get_all[0][1])
                    time.sleep(4)
                    self.clicker_manager.press_ecs()
                    time.sleep(1)
                    return True
                else:
                    for path in path_sa_detal_get_continue:
                        coord_sa_detal_get_continue = find_template_matches(path)
                        if coord_sa_detal_get_continue:
                            break
                    if coord_sa_detal_get_continue:
                        coord_end_gift = find_template_matches(path_sa_detal_end_gift)
                        if coord_end_gift and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET-LEG GIFT")
                            self.clicker_manager.click(coord_end_gift[0][0], coord_end_gift[0][1])
                            time.sleep(3)
                        else:
                            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET-PROPORTION-LEG GIFT")
                            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1185, target_y=445)
                            time.sleep(3)
                        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET-CONTINUE BTN FIND")
                        return True
                    else:
                        logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-GET-ALL OR CONINUE BTN UNDEFIND")
                        return False
            else:
                logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL-KONKURS BTN UNDEFIND")
                return False
        else:
            logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-DETAL BTN UNDEFIND")
            return False

    def take_sa_montaj(self, window):
        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ START FUNC")
        # Ищем кнопку конкурс снаряжения
        path_sa_montaj = resource_path(relative_path=self.locale.i10n('sa-montaj-icon'))
        path_sa_montaj_get = resource_path(relative_path=self.locale.i10n('sa-montaj-get'))

        path_sa_montaj_get_list = [
            path_sa_montaj_get
        ]

        path_sa_montaj_list = [
            path_sa_montaj
        ]
        coord_sa_montaj = []
        coord_sa_montaj_get = []

        scroll_times = 0
        while not self.task_manager.stop_event.is_set():
            if scroll_times > 5:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ TASK UNDEFIND")
                return True
            for path in path_sa_montaj_list:
                coord_sa_montaj = find_template_matches(path)
                if coord_sa_montaj:
                    break
            if coord_sa_montaj:
                break
            else:
                self.clicker_manager.proportion_move_cursor_in_window(target_x=75, target_y=390, window=window.window)
                time.sleep(1)
                self.clicker_manager.scroll(target=-75)
                scroll_times += 1
        if coord_sa_montaj and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ BTN FIND")
            self.clicker_manager.click(coord_sa_montaj[0][0], coord_sa_montaj[0][1])
            time.sleep(2)
            for path in path_sa_montaj_get_list:
                coord_sa_montaj_get = find_template_matches(path)
                if coord_sa_montaj_get:
                    break
            if coord_sa_montaj_get and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ-GET-ALL BTN FIND")
                self.clicker_manager.click(coord_sa_montaj_get[0][0], coord_sa_montaj_get[0][1])
                time.sleep(4)
                self.clicker_manager.press_ecs()
                time.sleep(1)
                return True
            else:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ-GET-ALL BTN UNDEFIND")
                return True
        else:
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MONTAJ BTN UNDEFIND")
            return False

    def take_sa_transport(self, window):
        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT START FUNC")
        # Ищем кнопку конкурс снаряжения
        path_sa_trans = resource_path(relative_path=self.locale.i10n('sa-transport'))
        path_sa_trans_get = resource_path(relative_path=self.locale.i10n('sa-transport-get'))

        path_sa_trans_list = [
            path_sa_trans
        ]

        path_sa_trans_get__list = [
            path_sa_trans_get
        ]
        coord_sa_trans = []
        coord_sa_trans_get = []

        scroll_times = 0
        while not self.task_manager.stop_event.is_set():
            if scroll_times > 5:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT TASK UNDEFIND")
                return True
            for path in path_sa_trans_list:
                coord_sa_trans = find_template_matches(path)
                if coord_sa_trans:
                    break
            if coord_sa_trans:
                break
            else:
                self.clicker_manager.proportion_move_cursor_in_window(target_x=75, target_y=390, window=window.window)
                time.sleep(1)
                self.clicker_manager.scroll(target=-75)
                scroll_times += 1
        if coord_sa_trans and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT BTN FIND")
            self.clicker_manager.click(coord_sa_trans[0][0], coord_sa_trans[0][1])
            time.sleep(2)
            for path in path_sa_trans_get__list:
                coord_sa_trans_get = find_template_matches(path)
                if coord_sa_trans_get:
                    break
            if coord_sa_trans_get and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT-GET-ALL BTN FIND")
                self.clicker_manager.click(coord_sa_trans_get[0][0], coord_sa_trans_get[0][1])
                time.sleep(4)
                self.clicker_manager.press_ecs()
                time.sleep(1)
                return True
            else:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT-GET-ALL BTN UNDEFIND")
                return True
        else:
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-TRANSPORT BTN UNDEFIND")
            return False

    def take_sa_mega(self, window):
        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA START FUNC")

        NEED_MISSION = False
        # Ищем кнопку конкурс снаряжения
        path_sa_mega = resource_path(relative_path=self.locale.i10n('sa-mega-icon1'))
        path_sa_mega2 = resource_path(relative_path=self.locale.i10n('sa-mega-icon2'))
        path_sa_mega3 = resource_path(relative_path=self.locale.i10n('sa-mega-icon3'))
        path_sa_mega_list = [
            path_sa_mega,
            path_sa_mega2,
            path_sa_mega3
        ]


        coord_sa_mega = []
        scroll_times = 0
        while not self.task_manager.stop_event.is_set():
            if scroll_times > 5:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA TASK UNDEFIND")
                return True

            for path in path_sa_mega_list:
                coord_sa_mega = find_template_matches(path)
                if coord_sa_mega:
                    break
            if coord_sa_mega:
                break
            else:
                self.clicker_manager.proportion_move_cursor_in_window(target_x=75, target_y=390, window=window.window)
                time.sleep(1)
                self.clicker_manager.scroll(target=-75)
                scroll_times += 1
        # Захожу в меню МЕГА
        if coord_sa_mega and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA BTN FIND")
            self.clicker_manager.click(coord_sa_mega[0][0], coord_sa_mega[0][1])
            time.sleep(2)
            path_add_misson = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-mega-add-mission.png")
            path_add_misson2 = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-mega-add-mission2.png")

            path_add_get = resource_path(relative_path=self.locale.i10n('sa-mega-get1'))
            path_add_get2 = resource_path(relative_path=self.locale.i10n('sa-mega-get2'))
            path_add_get_all = resource_path(relative_path=self.locale.i10n('sa-mega-get-all'))
            path_gather_mission = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-mega-gather-mission.png")
            path_mission_ok = resource_path(relative_path=self.locale.i10n('sa-mega-mission-ok'))

            path_get_list =[
                path_add_get,
                path_add_get2
            ]

            path_get_all_list =[
                path_add_get_all
            ]

            coord_get = []
            coord_get_all = []

            # Ищу меню миссий
            coord_mission_menu = find_template_matches(path_add_misson)
            if coord_mission_menu and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA MISSION MENU BTN FIND")
                NEED_MISSION = True
                self.clicker_manager.click(coord_mission_menu[0][0], coord_mission_menu[0][1])
                time.sleep(2)
            else:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA MISSION MENU BTN NOT FIND. PROPORTIONAL CLICK")
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=380, target_y=645)
                time.sleep(4)

            # Беру Миссию если надо
            if NEED_MISSION:
                coord_get_mission_menu = find_template_matches(path_add_misson2)
                if coord_get_mission_menu and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA GET MISSION MENU BTN FIND")
                    self.clicker_manager.click(coord_get_mission_menu[0][0], coord_get_mission_menu[0][1])
                    time.sleep(3)
                    coord_gather_mission = find_template_matches(path_gather_mission)
                    if coord_gather_mission and not self.task_manager.stop_event.is_set():
                        self.clicker_manager.click(coord_gather_mission[0][0], coord_gather_mission[0][1]+390)
                        time.sleep(2)
                        coord_mission_ok = find_template_matches(path_mission_ok)
                        if coord_mission_ok:
                            self.clicker_manager.click(coord_mission_ok[0][0], coord_mission_ok[0][1])
                            time.sleep(2)
                        else:
                            self.clicker_manager.press_ecs()
                            time.sleep(2)
                            self.clicker_manager.press_ecs()
                            time.sleep(2)


                    else:
                        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA GATHER MISSION BTN UNDERFINDFIND")
                        self.clicker_manager.press_ecs()
                        time.sleep(2)

            # Собираю выполненые миссии
            btn_get_underfind = 0
            while not self.task_manager.stop_event.is_set():
                if btn_get_underfind > 6:
                    self.clicker_manager.press_ecs()
                    time.sleep(2)
                    break

                for path in path_get_list:
                    coord_get = find_template_matches(path)
                    if coord_get and not self.task_manager.stop_event.is_set():
                        self.clicker_manager.click(coord_get[0][0], coord_get[0][1])
                        time.sleep(2)
                    else:
                        logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA GET BTN UNDERFIND")
                        btn_get_underfind+=1


            for path in path_get_all_list:
                coord_get_all = find_template_matches(path)
                if coord_get_all:
                    break

            if coord_get_all and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA GET ALL BTN FIND")
                self.clicker_manager.click(coord_get_all[0][0], coord_get_all[0][1])
                time.sleep(2)
                return True

            else:
                logger.info("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA GET ALL BTN UNDEFIND")
                path_end_gift = resource_path(relative_path="app\\windows\\shelter\\daily\\img\\sa-mega-end-gift.png")
                coord_end_gift = find_template_matches(path_end_gift)
                if coord_end_gift and not self.task_manager.stop_event.is_set():
                    self.clicker_manager.click(coord_end_gift[0][0], coord_end_gift[0][1])
                    time.sleep(3)
                return True

        else:
            logger.warning("GAME OBJECT SERVICE: DAILY: SPECAIAL ACTION: SA-MEGA BTN UNDEFIND")
            return False



# ======================== HEALER ===================== #
    @check_stop_func
    def healer(self, task):
        path_pex = resource_path(relative_path="app\\windows\\shelter\\healer\\img\\pex.png")
        path_strlk = resource_path(relative_path="app\\windows\\shelter\\healer\\img\\strl.png")
        path_vsad = resource_path(relative_path="app\\windows\\shelter\\healer\\img\\svad.png")
        path_inj = resource_path(relative_path="app\\windows\\shelter\\healer\\img\\inj.png")
        self.go_to_region()

        time.sleep(2)
        # сворачиванием ненужные иконки вверху окна
        self.hide_discont()
        count = 0
        while not self.task_manager.stop_event.is_set():

            if count > 4:
                logger.info("GAME OBJECT SERVICE: HEALER: TASK IS END")
                self.go_to_shelter()
                break

            self.go_to_shelter()
            # Ищем значок лечения на больницей
            path_hospital_btn = resource_path(relative_path="app\\img\\game_button\\heal_button.png")
            coord_hospital = find_template_matches(path_hospital_btn)

            if coord_hospital and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: HEALER: FIND HOSPITAL")
                hospital = filter_coordinates(coord_hospital, threshold=40)
                # Кликаем на кнопку лечения на больницей
                self.clicker_manager.click(hospital[0][0], hospital[0][1])
                time.sleep(3)

                # Ищем стрелочку вниз чтобы убрать лечение всех войск
                path_arrow_down = resource_path(relative_path="app\\img\\game_button\\arrow_down_hospital.png")
                coord_arrow = find_template_matches(path_arrow_down)

                path_heal_res = resource_path(relative_path=self.locale.i10n(message_id="heal-resource1"))
                path_heal_res2 = resource_path(relative_path=self.locale.i10n(message_id="heal-resource2"))

                path_heal_res =[
                    path_heal_res,
                    path_heal_res2
                ]
                # Ищем лечение за ресурсы а не банки
                for path in path_heal_res:
                    coord_res = find_template_matches(path)
                    if coord_res:
                        logger.info("GAME OBJECT SERVICE: HEALER: RESOURSE WINDOW IN SCREEN")
                        self.clicker_manager.click(coord_res[0][0], coord_res[0][1])
                        time.sleep(2)
                        break

                # Кликаем на стрелку вниз очистив выбор всех войск
                if coord_arrow and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: HEALER: FIND ARROW DOWN BTN")
                    self.clicker_manager.click(coord_arrow[0][0], coord_arrow[0][1])
                    time.sleep(1)

                    # Определяем расположение иконок
                    coord_pex = find_template_matches(path_pex, threshold=0.7)
                    coord_strlk = find_template_matches(path_strlk, threshold=0.7)
                    coord_vsad = find_template_matches(path_vsad, threshold=0.7)
                    coord_inj = find_template_matches(path_inj, threshold=0.7)

                    # Кликаем в окошко ввода количества войск для лечения в зависимости от задания
                    if task['pex'] and coord_pex and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HEALER: PEX TROOPS HEAL")
                        self.clicker_manager.click(coord_pex[0][0]+410, coord_pex[0][1])
                        time.sleep(0.3)
                        self.clicker_manager.click_at_current_position()
                    elif task['strl'] and coord_strlk and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HEALER: STRLK TROOPS HEAL")
                        self.clicker_manager.click(coord_strlk[0][0]+410, coord_strlk[0][1])
                        time.sleep(0.3)
                        self.clicker_manager.click_at_current_position()
                    elif task['vsad'] and coord_vsad and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HEALER: VSAD TROOPS HEAL")
                        self.clicker_manager.click(coord_vsad[0][0]+410, coord_vsad[0][1])
                        time.sleep(0.3)
                        self.clicker_manager.click_at_current_position()
                    elif task['inj'] and coord_inj and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HEALER: INJ TROOPS HEAL")
                        self.clicker_manager.click(coord_inj[0][0]+410, coord_inj[0][1])
                        time.sleep(0.3)
                        self.clicker_manager.click_at_current_position()
                    else:
                        logger.info("GAME OBJECT SERVICE: HEALER: TROOPS UNDEFIND. COUNT: %s", count)
                        count+=1
                        continue

                    # Удаляем на всякий случай войска
                    self.clicker_manager.press_backspace(8)
                    # Вводим количество войск из self.heal_data['count_unit']
                    self.clicker_manager.input_numbers(str(task['count_unit']))

                    # Клик на кнопку лечить
                    path_heal = resource_path(relative_path=self.locale.i10n(message_id="heal-button"))
                    coord_heal = find_template_matches(path_heal)
                    if coord_heal and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HEALER: FIND HEAL BTN")
                        self.clicker_manager.click(coord_heal[0][0], coord_heal[0][1])
                        time.sleep(3)

                        # # Клик по ручке над больничкой
                        # logger.info("GAME OBJECT SERVICE: HEALER: CLICK TO HELP HAND")
                        # self.clicker_manager.click(hospital[0][0], hospital[0][1])
                        # time.sleep(1)

                        # Ожидаем окончания лечения пока шприч исчезнет
                        while not self.task_manager.stop_event.is_set():
                            path_wpric = resource_path(relative_path="app\\img\\game_button\\wpric.png")
                            if find_template_matches(path_wpric):
                                self.click_hand()
                                time.sleep(3)
                                logger.info(msg="GAME OBJECT SERVICE: HEALER: WAIT TO END WPRIC")
                                continue
                            else:
                                logger.info(msg="GAME OBJECT SERVICE: HEALER: WPRIC END")
                                break

                        # Клик по вылеченым войскам
                        logger.info("GAME OBJECT SERVICE: HEALER: CLICK TO LIVED TROOPS")
                        self.clicker_manager.click(hospital[0][0], hospital[0][1])
                        time.sleep(1.5)
                        count = 0

                    else:
                        logger.info(msg="GAME OBJECT SERVICE: HEALER: HEAL BTN UNDEFIND")
                        continue

                else:
                    logger.info(msg="GAME OBJECT SERVICE: HEALER: ARROW DOWN UNDEFIND")
                    continue
            else:
                count += 1
                logger.info("GAME OBJECT SERVICE: HEALER: HOSPITAL UNDEFIND. TRY COUNT: %s", count)


# =========================== HUNT ================================== #
    @check_stop_func
    def hunt_afk_algorithm(self, window):
        logger.info("GAME OBJECT SERVICE: HUNT: STARTED ALGORITHM")
        self.go_to_shelter()
        time.sleep(5)
        path_in_game = resource_path(relative_path=self.locale.i10n('hunt-in-game'))
        coord_in_game = find_template_matches(path_in_game, threshold=0.7)
        # Проверяю находится ли в игре
        if coord_in_game and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: HUNT: HUNT IN PROCESS. SLEEP 20 SEC.")
            # Засыпаю на 20 сек
            time.sleep(20)
            coord_in_game = find_template_matches(path_in_game, threshold=0.7)
            # Проверяю находится ли все еще в игре. Если в игре, то иду в следующее окно
            if coord_in_game and not self.task_manager.stop_event.is_set():
                return

        self.go_to_company()
        time.sleep(3)
        # Ищу меню охоты
        path_hunt = resource_path(relative_path="app\\img\\game_button\\company\\hunt.png")
        coord_hunt = find_template_matches(path_hunt)
        if coord_hunt and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: HUNT: HUNT MENU FIND")
            self.clicker_manager.click(coord_hunt[0][0], coord_hunt[0][1])
            time.sleep(2)
            path_podbor = resource_path(relative_path=self.locale.i10n('hunt-search-game'))
            coord_podbor = find_template_matches(path_podbor)
            # Ищу кнопку подбор
            if coord_podbor and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: HUNT: PODBOR BTN FIND")
                self.clicker_manager.click(coord_podbor[0][0], coord_podbor[0][1])
                time.sleep(1)
                self.clicker_manager.press_ecs()
                time.sleep(1)
                self.clicker_manager.press_ecs()
                time.sleep(4)
                path_find_match = resource_path(relative_path=self.locale.i10n('hunt-find-match'))
                path_otmena = resource_path(relative_path=self.locale.i10n('hunt-otmena'))
                path_exit_from_game = resource_path(relative_path="app\\windows\\shelter\\hunt\\img\\exit-from-game.png")
                path_game_shop = resource_path(relative_path="app\\windows\\shelter\\hunt\\img\\shop-in-game.png")
                # Жду когда закончится подбор
                count_fail = 0
                while not self.task_manager.stop_event.is_set():
                    if count_fail > 15:
                        break
                    # Проверяю не начался ли gодбор неожиданно, вдруг меня закинуло в игру
                    coord_shop = find_template_matches(path_game_shop)
                    # Проверяю появилась ли иконка магазина уже на поле битвы
                    if coord_shop and not self.task_manager.stop_event.is_set():
                        time.sleep(1)
                        coord_exit = find_template_matches(path_exit_from_game)
                        # Ищу кнопку назад чтобы свернуть поле битвы
                        if coord_exit and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: HUNT: JOIN IN GAME. FIND EXIT BUTTON")
                            self.clicker_manager.click(coord_exit[0][0], coord_exit[0][1])
                            time.sleep(3)
                            # Проверяю в процессе ли игры
                            coord_in_game = find_template_matches(path_in_game, threshold=0.7)
                            if coord_in_game and not self.task_manager.stop_event.is_set():
                                time.sleep(1)
                                return
                    coord_find_match = find_template_matches(path_find_match)
                    # Проверяю статус что идёт подбор
                    if coord_find_match and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: HUNT: WAIT TO END FIND MATCH")
                        time.sleep(3)
                        continue
                    # Тут статус побора исчез, ищу кнопку отмена чтобы не заходить в поле битвы
                    else:
                        logger.info("GAME OBJECT SERVICE: HUNT: FIND MATCH")
                        coord_otmena = find_template_matches(path_otmena)

                        if coord_otmena and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: HUNT: FIND OTMENA BTN")
                            self.clicker_manager.click(coord_otmena[0][0], coord_otmena[0][1])
                            time.sleep(2)
                            logger.info("GAME OBJECT SERVICE: HUNT: LOOP END")
                            return
                        else:
                            self.go_to_shelter()
                            count_fail += 1
                            time.sleep(2)
            else:
                logger.info("GAME OBJECT SERVICE: HUNT: PODBOR BTN UNDEFIND")
                self.go_to_shelter()
                return
        else:
            logger.info("GAME OBJECT SERVICE: HUNT: HUNT MENU UNDEFIND")
            self.go_to_shelter()
            return


# ============================= WATER WAR ================================= #
    @check_stop_func
    def water_algorithm(self, window):
        # Проверяю нахожусь ли я уже в Разделе война за воду
        path_podbor_btn = resource_path(relative_path=self.locale.i10n('ww-porbor'))
        coord_menu = find_template_matches(path_podbor_btn)
        if coord_menu and not self.task_manager.stop_event.is_set():
            pass
        else:
            self.go_to_shelter()
            time.sleep(3)
            if not self.task_manager.stop_event.is_set():
                # Захожу в раздел ивентов
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1200, target_y=120)
                time.sleep(3)
                # Перемещаю курсор чтобы скролить вниз и искать Войну за воду
                self.clicker_manager.proportion_move_cursor_in_window(window=window.window, target_x=180, target_y=510)
                time.sleep(1)
                path_water_btn = resource_path(relative_path=self.locale.i10n('ww-water-btn1'))
                path_water_btn2 = resource_path(relative_path=self.locale.i10n('ww-water-btn2'))
                path_list_btn = [
                    path_water_btn,
                    path_water_btn2
                    ]
                in_menu = False
                while not self.task_manager.stop_event.is_set():
                    if in_menu:
                        break
                    for path in path_list_btn:
                        coord_water_btn = find_template_matches(path)
                        if coord_water_btn:
                            self.clicker_manager.click(coord_water_btn[0][0], coord_water_btn[0][1])
                            time.sleep(2)
                            in_menu = True
                            break
                        else:
                            self.clicker_manager.scroll(-75)

        coord_podbor = find_template_matches(path_podbor_btn)
        if coord_podbor and not self.task_manager.stop_event.is_set():
            self.clicker_manager.click(coord_podbor[0][0], coord_podbor[0][1])
            time.sleep(2)

        path_cancel_podbor = resource_path(relative_path=self.locale.i10n('ww-cancel-podbor'))
        path_ready = resource_path(relative_path=self.locale.i10n('ww-ready'))
        path_vs = resource_path(relative_path="app\\windows\\shelter\\water\\img\\vs.png")
        path_end_battle = resource_path(relative_path=self.locale.i10n('ww-end'))
        while not self.task_manager.stop_event.is_set():
            coord_vs = find_template_matches(path_vs)
            if coord_vs and not self.task_manager.stop_event.is_set():
                break
            coord_cancel_podbor = find_template_matches(path_cancel_podbor)
            if coord_cancel_podbor and not self.task_manager.stop_event.is_set():
                logger.info(msg="GAME OBJECT SERVICE: WATER: CANCEL PODBOR FIND - GOOD. WAIT READY")
                time.sleep(5)
            else:
                coord_ready = find_template_matches(path_ready)
                if coord_ready and not self.task_manager.stop_event.is_set():
                    logger.info(msg="GAME OBJECT SERVICE: WATER: READY PODBOR FIND")
                    self.clicker_manager.click(coord_ready[0][0], coord_ready[0][1])
                    time.sleep(2)


        while not self.task_manager.stop_event.is_set():
            time.sleep(9)

            coord_vs = find_template_matches(path_vs)
            if coord_vs and not self.task_manager.stop_event.is_set():
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1130, target_y=405)
                time.sleep(2)

                path_end = resource_path(relative_path=self.locale.i10n('ww-end-battle'))
                coord_end = find_template_matches(path_end)
                if coord_end and not self.task_manager.stop_event.is_set():
                    self.clicker_manager.click(coord_end[0][0], coord_end[0][1])
                    continue
            else:
                time.sleep(6)
                coord_end_battle = find_template_matches(path_end_battle)
                if coord_end_battle:
                    self.clicker_manager.proportion_click_in_window(window=window.window, target_x=630, target_y=670)
                    time.sleep(6)
                else:
                    continue

            path_skip = resource_path(relative_path=self.locale.i10n('ww-skip-end-battle'))
            coord_skip = find_template_matches(path_skip)
            if coord_skip and not self.task_manager.stop_event.is_set():
                self.clicker_manager.click(coord_skip[0][0], coord_skip[0][1])
                time.sleep(8)
                path_exit = resource_path(relative_path=self.locale.i10n('ww-exit'))
                coord_exit = find_template_matches(path_exit)
                if coord_exit and not self.task_manager.stop_event.is_set():
                    self.clicker_manager.click(coord_exit[0][0], coord_exit[0][1])
                    time.sleep(8)
                    break


# =============================== RALLY ======================================#

    # self.rally_started = None
    def rally_step_0(self,window, task):
        self.rally_task = task
        logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-0]: RALLY ALGORITHM STARTED GO TO STEP-1")
        return self.rally_step_1(window=window)
    # Проверка остатка сборов и свобен ли отряд
    @check_stop_func
    def rally_step_1(self, window):
        if self.rally_task['fail_count'] == 8:
            return
        if self.rally_task['count_rally'] == 0:
            logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-1]: COUNT RALLY 0. END TASK.")
            return
        if self.rally_task['max_lvl']-self.rally_task['down_count'] <= 0:
            self.rally_task['down_count'] = 0
        self.go_to_region()
        time.sleep(3)
        if self.check_free_group():
            time.sleep(1)
            logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-1]: FIND FREE GROUP. GO TO STEP-2")
            # проверить какая задержка ралли и прошло ли время
            return self.rally_step_2(window=window)
        else:
            logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-1]: ALL GROUP USED - SLEEP 30 SEC")
            time.sleep(10)
            logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-1]: GO TO STEP-1")
            return self.rally_step_1(window=window)

    # Нажатие на лупу и выбор разума
    @check_stop_func
    def rally_step_2(self, window):
        path_loup = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\loups.png")

        coord_loup = find_template_matches(path_loup)
        if coord_loup and not self.task_manager.stop_event.is_set():
            self.clicker_manager.click(coord_loup[0][0], coord_loup[0][1])
            time.sleep(3)
        else:
            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=45,target_y=480)
            time.sleep(3)

        logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-2]: GO TO STEP-3")
        return self.rally_step_3(window=window)

    # Выбор уровня
    @check_stop_func
    def rally_step_3(self, window):
        # path_razum = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\razum.png")

        # coord_razum = find_template_matches(path_razum)
        # if coord_razum and not self.task_manager.stop_event.is_set():
        #     logger.info(msg="GAME OBJECT SERVICE: RALLY[STEP-3]: FIND RAZUM")
        #     self.clicker_manager.click(coord_razum[0][0], coord_razum[0][1])
        #     time.sleep(4)


        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=385,target_y=650)
        path_lvl_razum = {
            1: resource_path(self.locale.i10n('rally-lvl1')),
            2: resource_path(self.locale.i10n('rally-lvl2')),
            3: resource_path(self.locale.i10n('rally-lvl3')),
            4: resource_path(self.locale.i10n('rally-lvl4')),
            5: resource_path(self.locale.i10n('rally-lvl5')),
            6: resource_path(self.locale.i10n('rally-lvl6')),
            7: resource_path(self.locale.i10n('rally-lvl7')),
        }
        path_lvlup = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlup.png")
        path_lvldown = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvldown.png")
        path_lvlmax = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlmax.png")
        path_lvlmin = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlmin.png")
        current_lvl = 0
        for lvl, path in path_lvl_razum.items():
            time.sleep(0.5)
            if self.task_manager.stop_event.is_set():
                break
            coord_lvl = find_template_matches(path, threshold=0.95)
            if coord_lvl:
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: GET CURRENT LVL: %s", lvl)
                current_lvl = lvl
                break

        if current_lvl == 0:
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: FAILED GET CURRENT LVL. GO TO STEP - 1")
            return self.rally_step_1(window=window)

        if current_lvl > self.rally_task['max_lvl']:
            # проверить не минимальный ли
            coord_lvlmin = find_template_matches_color(path_lvlmin, threshold=0.95)
            if coord_lvlmin and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL MIN DETECTED. SKIP CHANGE")
            else:
                coord_lvldown = find_template_matches_color(path_lvldown)
                if coord_lvldown and not self.task_manager.stop_event.is_set():
                    for i in range(current_lvl-self.rally_task['max_lvl']):
                        if self.task_manager.stop_event.is_set():
                            break
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL DOWN")
                        self.clicker_manager.click(coord_lvldown[0][0], coord_lvldown[0][1])
                        time.sleep(1)
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: FAIL DETECTED LVL DOWN")

        if current_lvl < self.rally_task['max_lvl']:
            coord_lvlmax = find_template_matches_color(path_lvlmax, threshold=0.95)
            if coord_lvlmax:
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL MAX DETECTED. SKIP CHANGE")
            else:
                coord_lvlup = find_template_matches_color(path_lvlup)
                if coord_lvlup and not self.task_manager.stop_event.is_set():
                    for i in range(abs(current_lvl-self.rally_task['max_lvl'])):
                        if self.task_manager.stop_event.is_set():
                            break
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL UP")
                        self.clicker_manager.click(coord_lvlup[0][0], coord_lvlup[0][1])
                        time.sleep(1)
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: FAIL DETECTED LVL UP")


        if current_lvl == self.rally_task['max_lvl']:
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL IS GOOD")



        if self.rally_task['down_triger']:
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: DOWN TRIGGER IS TRUE")
            coord_lvldown = find_template_simple(path_lvldown)
            if coord_lvldown and not self.task_manager.stop_event.is_set():
                for i in range(self.rally_task['down_count']):
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: LVL DOWN")
                    self.clicker_manager.click(coord_lvldown[0][0], coord_lvldown[0][1])
                    time.sleep(1)
        logger.info("GAME OBJECT SERVICE: RALLY[STEP-3]: GO TO STEP 4")
        return self.rally_step_4(window=window)

    # Нажатие кнопки поиск в меню выбор
    @check_stop_func
    def rally_step_4(self, window):
        path_poisk = resource_path(relative_path=self.locale.i10n('rally-poisk'))
        coord_poisk = find_template_matches_color(path_poisk)
        if coord_poisk and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-4]: POISK DETECTED")
            self.clicker_manager.click(coord_poisk[0][0], coord_poisk[0][1])
            time.sleep(6)

        logger.info("GAME OBJECT SERVICE: RALLY[STEP-4]: GO TO STEP 5")
        return self.rally_step_5(window=window)

    # Нажимаем на центр экрана(на разум) чтобы появилась кнопка
    @check_stop_func
    def rally_step_5(self, window):
        # Нажать на центр экрана чтоб выбрать разум 640 390
        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=640, target_y=390)
        time.sleep(3)
        logger.info("GAME OBJECT SERVICE: RALLY[STEP-5]: GO TO STEP 6")
        return self.rally_step_6(window=window)

    # Ищем кнопку СБОР
    @check_stop_func
    def rally_step_6(self, window):
        # Найти кнопку сбор
        path_sbor = resource_path(relative_path=self.locale.i10n('rally-sbor'))
        path_sbor_list  = [
            path_sbor
        ]
        coord_sbor = []
        for path in path_sbor_list:
            coord_sbor = find_template_matches(path)
            if coord_sbor and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-6]: FIND SBOR BUTTON")
                self.clicker_manager.click(coord_sbor[0][0], coord_sbor[0][1])
                time.sleep(3)
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-6]: GO TO STEP 7")
                return self.rally_step_7(window=window)
            else:
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-6]: SBOR BUTTON UNDEFIND")
                self.rally_task['down_triger'] = True
                self.rally_task['down_count'] += 1
                self.rally_task['fail_count'] += 1
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-6]: GO TO STEP 1")
                return self.rally_step_1(window=window)


    # проверяем временную галочку
    @check_stop_func
    def rally_step_7(self, window):
        path_check_sbor_time_menu = resource_path(relative_path=self.locale.i10n('rally-attack-check'))
        coord_time_menu = find_template_matches(path_check_sbor_time_menu)
        if coord_time_menu and not self.task_manager.stop_event.is_set():
            # Найти галочку на 2 или на 4 или на 5 минут
            path_2m_time_check = resource_path(relative_path=self.locale.i10n('rally-2m-check'))
            path_2m_time_empty = resource_path(relative_path=self.locale.i10n('rally-2m-empty'))
            path_4m_time_check = resource_path(relative_path=self.locale.i10n('rally-4m-check'))
            path_4m_time_empty = resource_path(relative_path=self.locale.i10n('rally-4m-empty'))
            path_5m_time_check = resource_path(relative_path=self.locale.i10n('rally-5m-check'))
            path_5m_time_empty = resource_path(relative_path=self.locale.i10n('rally-5m-empty'))

            path_2m_list = [
                path_2m_time_check,
                path_2m_time_empty
            ]
            path_4m_list = [
                path_4m_time_check,
                path_4m_time_empty
            ]
            path_5m_list = [
                path_5m_time_check,
                path_5m_time_empty
            ]
            coord_times = []
            TIME_STATUS = False
            fail_count = 0
            while not self.task_manager.stop_event.is_set():
                if fail_count == 2:
                    break

                for path in path_2m_list:
                    coord_times = find_template_matches(path, threshold=0.95)
                    if coord_times and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: FIND 2M TIME")
                        self.clicker_manager.click(coord_times[0][0], coord_times[0][1])
                        time.sleep(1)
                        TIME_STATUS = True
                        break
                    else:
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: 2M TIME UNDEFIND")

                if TIME_STATUS:
                    fail_count = 0
                    break

                for path in path_4m_list:
                    coord_times = find_template_matches(path, threshold=0.95)
                    if coord_times and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: FIND 4M TIME")
                        self.clicker_manager.click(coord_times[0][0], coord_times[0][1])
                        time.sleep(1)
                        TIME_STATUS = True
                        break
                    else:
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: 4M TIME UNDEFIND")

                if TIME_STATUS:
                    fail_count = 0
                    break

                for path in path_5m_list:
                    coord_times = find_template_matches(path, threshold=0.95)
                    if coord_times and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: FIND 5M TIME")
                        self.clicker_manager.click(coord_times[0][0], coord_times[0][1])
                        time.sleep(1)
                        TIME_STATUS = True
                        break
                    else:
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: 5M TIME UNDEFIND")

                if TIME_STATUS:
                    fail_count = 0
                    break

                fail_count += 1

            if TIME_STATUS:
                path_sbor_time = resource_path(relative_path=self.locale.i10n('rally-sbor-time'))
                path_sbor_time_list = [
                    path_sbor_time
                ]
                coord_sbor_time = []
                for path in path_sbor_time_list:
                    coord_sbor_time = find_template_matches(path)
                    if coord_sbor_time:
                        break
                if coord_sbor_time and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: SBOR-TIME FIND")
                    self.clicker_manager.click(coord_sbor_time[0][0], coord_sbor_time[0][1])
                    time.sleep(2)
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: GO TO STEP 8")
                    return self.rally_step_8(window)
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: SBOR-TIME UNDEFIND")
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: GO TO STEP 1")
                    return self.rally_step_1(window=window)
        else:
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: RAZUS IS BUSY ANOTHER RALLY")
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: DOWN TRIGGER ADDED")
            self.rally_task['down_triger'] = True
            self.rally_task['down_count'] += 1
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-7]: GO TO STEP 1")
            return self.rally_step_1(window=window)

    # Нажимаем Маршу
    @check_stop_func
    def rally_step_8(self, window):
        path_marsh = resource_path(relative_path=self.locale.i10n('rally-marsh'))
        path_marsh_list = [
            path_marsh
        ]
        coord_marsh = []
        for path in path_marsh_list:
            coord_marsh = find_template_matches(path)
            if coord_marsh:
                break
        if coord_marsh and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-8]: FIND MARSH BUTTON")
            self.clicker_manager.click(coord_marsh[0][0], coord_marsh[0][1])
            time.sleep(3)
            path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
            path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
            # Проверяю появилось ли окно то что нет энергии
            coord_green_use = find_template_matches(path_green_use)
            if coord_green_use and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: RALLY[STEP-8]: NO HAVE ENERGY")
                green_count = 0
                while not self.task_manager.stop_event.is_set():
                    if green_count == 15:
                        self.task_manager.stop_event.set()
                        return
                    coord_green_half = find_template_matches(path_green_half_empty)
                    if coord_green_half and not self.task_manager.stop_event.is_set():
                        coord_green_use_update = find_template_matches(path_green_use)
                        filter_coord = filter_coordinates(coord_green_use_update)
                        for x, y in filter_coord:
                            self.clicker_manager.click(x, y)
                            time.sleep(0.5)
                        green_count += 1
                    else:
                        self.clicker_manager.press_ecs()
                        time.sleep(2)
                        self.clicker_manager.click(coord_marsh[0][0], coord_marsh[0][1])
                        time.sleep(2)
                        break
            self.rally_task['down_triger'] = False
            self.rally_task['down_count'] = 0
            self.rally_task['fail_count'] = 0
            self.rally_task['start_time_rally'] = datetime.datetime.now()
            self.rally_task['count_rally'] -= 1
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-8]: GO TO STEP-9")
            # Выход в меню проверки что делать дальше после сбора
            return self.rally_step_9(window)

        else:
            self.rally_task['fail_count'] += 1
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-8]: MARSH BUTTON UNDEFIND")
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-8]: GO TO STEP 1")
            return self.rally_step_1(window=window)
        # ТУТ ОБРАБОТКА ТАЙМИНГА И СБРОСА ВСЕХ ФЛАГОВ

    # Меню распределения дальнейших действий после начала сбора
    @check_stop_func
    def rally_step_9(self, window):
        # Проверяем триггер нужно ли входит ьв чужие сборы
        if self.rally_task['entry_rally']:
            while not self.task_manager.stop_event.is_set():


                # Прошло 8 минут. Пора делать новый сбор
                time_dif = datetime.datetime.now() - self.rally_task['start_time_rally']
                if  time_dif.total_seconds() >= 480:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: TIME 8M END. ENTRY RALLY END")
                    break


                self.go_to_region()

                if not self.check_free_group():
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: ALL GROUP IS BUSY. SLEEP 30 SEC. RESTART ENTRY RALLY")
                    time.sleep(30)
                    continue

                time.sleep(2)
                self.go_to_ally()
                time.sleep(2)
                path_entry_rally = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\entry-rally.png")
                coord_entry_rally = find_template_matches(path_entry_rally, threshold=0.90)
                if coord_entry_rally and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: ENTRY RALLY MENU")
                    self.clicker_manager.click(coord_entry_rally[0][0], coord_entry_rally[0][1])
                    time.sleep(2)
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: RALLY MENU UNDEFIND")
                    self.go_to_region()
                    time.sleep(2)
                    continue
                ENRTY_STATUS = False
                for _ in range(10):
                    path_entry_plus = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\entry-rally-plus.png")
                    coord_entry_plus = find_template_matches(path_entry_plus, threshold=0.90)
                    if coord_entry_plus and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: ENTRY RALLY PLUS")
                        self.clicker_manager.click(coord_entry_plus[0][0], coord_entry_plus[0][1])
                        ENRTY_STATUS = True
                        time.sleep(5)
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: SLEEP 5")
                        break
                    self.clicker_manager.scroll(target=-25)
                    time.sleep(1)
                if ENRTY_STATUS:
                    path_entry_create_group = resource_path(relative_path=self.locale.i10n('entry-rally-create-group'))
                    coord_entry_create_group = find_template_matches(path_entry_create_group, threshold=0.90)
                    if coord_entry_create_group and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: CREATE GROUP")
                        self.clicker_manager.click(coord_entry_create_group[0][0], coord_entry_create_group[0][1])
                        time.sleep(2)
                        path_entry_marsh = resource_path(relative_path=self.locale.i10n('entry-rally-marsh'))
                        coord_entry_marsh = find_template_matches(path_entry_marsh, threshold=0.90)
                        if coord_entry_marsh and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: MARSH")
                            self.clicker_manager.click(coord_entry_marsh[0][0], coord_entry_marsh[0][1])
                            time.sleep(2)
                            path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
                            path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
                            # Проверяю появилось ли окно то что нет энергии
                            coord_green_use = find_template_matches(path_green_use)
                            if coord_green_use and not self.task_manager.stop_event.is_set():
                                logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: NO HAVE ENERGY")
                                green_count = 0
                                while not self.task_manager.stop_event.is_set():
                                    if green_count == 15:
                                        self.task_manager.stop_event.set()
                                        return
                                    coord_green_half = find_template_matches(path_green_half_empty)
                                    if coord_green_half and not self.task_manager.stop_event.is_set():
                                        coord_green_use_update = find_template_matches(path_green_use)
                                        filter_coord = filter_coordinates(coord_green_use_update)
                                        for x, y in filter_coord:
                                            self.clicker_manager.click(x, y)
                                            time.sleep(0.5)
                                        green_count += 1
                                    else:
                                        self.clicker_manager.press_ecs()
                                        time.sleep(2)
                                        self.clicker_manager.click(coord_entry_marsh[0][0], coord_entry_marsh[0][1])
                                        time.sleep(2)
                                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: ENTRY IS SUCCESFULL. RESTART ENTRY RALLY")
                                        break
                        # Не нашел МАРШ
                        else:
                            time.sleep(10)
                            logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: MARSH UNDEFIND. RESTART ENTRY RALLY")
                            continue

                    # Не нашел создать отряд
                    else:
                        logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: CREATE GROUP UNDEFIND. RESTART ENTRY RALLY.SLEEP 10 SEC")
                        time.sleep(10)
                        continue
                # Не нашел плюс
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: PLUS UNDEFIND. RESTART ENTRY RALLY. SLEEP 20 SEC")
                    time.sleep(20)
                    continue

            logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: GO TO STEP 1")
            self.rally_step_1(window=window)
        else:
            while not self.task_manager.stop_event.is_set():
                time_dif = datetime.datetime.now() - self.rally_task['start_time_rally']
                if  time_dif.total_seconds() >= 480:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: TIME DELAY 8M END.")
                    break
                else:
                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: TIME %smin %ss to END. SLEEP 30 SEC", int((480-time_dif.total_seconds())//60), int((60-time_dif.total_seconds())%60))
                    time.sleep(30)
            logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: GO TO STEP 1")
            return self.rally_step_1(window=window)



# ========================== TRANSFER ============================ #
    def transfer_step_0(self, window, task):
        self.transfer_task = task
        self.go_to_shelter()
        time.sleep(2)
        self.go_to_region()
        time.sleep(2)
        if not self.transfer_task['hide_discount']:
            self.hide_discont()
            self.transfer_task['hide_discount'] = True
        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-0]: HIDE DISCOUNT IS DONE")
        time.sleep(2)

        logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-0]: GO TO STEP-1")
        self.transfer_step_1(window=window)

    @check_stop_func
    def transfer_step_1(self, window):
        self.go_to_region()
        path_loup = resource_path(relative_path="app\\windows\\shelter\\transfer\\img\\loup-coord.png")
        path_loup_list = [
                    path_loup
                ]
        coord_loup = []
        for path in path_loup_list:
            coord_loup = find_template_simple(path, threshold=0.7)
            if coord_loup:
                break
        if coord_loup and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-1]: LOUP FIND")
            self.clicker_manager.click(coord_loup[0][0], coord_loup[0][1])
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-1]: GO TO STEP-2")
            time.sleep(2)
            self.transfer_step_2(window=window)

        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-1]: LOUP UNDEFIND. PROPORTIONAL CLICK")
            self.clicker_manager.proportion_click_in_window(window.window, target_x=435, target_y=55)
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-1]: GO TO STEP-2")
            time.sleep(2)
            self.transfer_step_2(window=window)

    @check_stop_func
    def transfer_step_2(self, window):
        path_x = resource_path(relative_path="app\\windows\\shelter\\transfer\\img\\x.png")
        path_y = resource_path(relative_path="app\\windows\\shelter\\transfer\\img\\y.png")
        path_find = resource_path(relative_path="app\\windows\\shelter\\transfer\\img\\find.png")

        coord_x = find_template_simple(path_x)
        if coord_x and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: X FIND")
            self.clicker_manager.click(coord_x[0][0]+70, coord_x[0][1])
            time.sleep(1)
            self.clicker_manager.press_backspace(times=4)
            time.sleep(1)
            self.clicker_manager.input_numbers(numbers=self.transfer_task['coord'][0])
            time.sleep(1)
        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: X UNDEFIND")
            return

        coord_y = find_template_simple(path_y, threshold=0.95)
        if coord_y and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: Y FIND")
            self.clicker_manager.click(coord_y[0][0]+70, coord_y[0][1])
            time.sleep(1)
            self.clicker_manager.press_backspace(times=4)
            time.sleep(1)
            self.clicker_manager.input_numbers(numbers=self.transfer_task['coord'][1])
            time.sleep(1)
        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: Y UNDEFIND")
            return

        coord_find = find_template_matches(path_find)
        if coord_find and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: BTN FIND DETECTED")
            self.clicker_manager.click(coord_find[0][0], coord_find[0][1])
            time.sleep(5)
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: GO TO STEP-3")
            self.transfer_step_3(window=window)
        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-2]: BTN FIND UNDEFIND")
            return


    @check_stop_func
    def transfer_step_3(self, window, task=None):
        if task is None:
            pass
        else:
            self.transfer_task = task
        if not self.check_free_group():
            return
        time.sleep(2)
        logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: PROPORTIONAL CLICK CENTER")
        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=720, target_y=350)
        time.sleep(4)
        path_transfer_menu = resource_path(relative_path=self.locale.i10n('transfer-menu'))
        coord_transfer_menu = find_template_matches(path_transfer_menu)
        if coord_transfer_menu and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: FIND TRANSFER MENU")
            self.clicker_manager.click(coord_transfer_menu[0][0], coord_transfer_menu[0][1])
            time.sleep(4)
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: GO TO STEP-4")
            self.transfer_step_4(window=window)
        else:
            # Тут кнопка на убежите СНАБЖЕНИЕ РЕСУРСАМИ не найдено
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: TRANSFER MENU UNDEFIND")
            self.transfer_task['screen_status'] = None
            self.transfer_task['fail_count'] += 1
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: WINDOW ID: %s FAIL COUNT UP TO: %s", self.transfer_task['id'], self.transfer_task['fail_count'])
            if self.transfer_task['fail_count'] >= 3:
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: FAIL COUNT == 3, DROP Fail count, GO TO NEXT WINDOW")
                self.transfer_task['fail_count'] = 0
                return
            else:
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-3]: GO TO STEP-1")
                self.transfer_step_1(window=window)

    @check_stop_func
    def transfer_step_4(self, window):


        # Проверка достигнут ли лимит убежища по поставкам
        path_limit = resource_path(relative_path=self.locale.i10n('transfer-limit'))
        coord_limit = find_template_simple(path_limit, threshold=0.97)
        if coord_limit:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: WINDOW ID:%s. TASK LIMIT OUT", self.transfer_task['id'])
            self.transfer_task['task_status'] = True
            self.clicker_manager.press_ecs()
            return

        # Проверка достигнут ли лимит по отправке
        path_transferout = resource_path(relative_path=self.locale.i10n('transfer-out'))
        coord_transferout = find_template_simple(path_transferout, threshold=0.95)
        if coord_transferout:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: WINDOW ID:%s .TRANSFER LIMIT OUT", self.transfer_task['id'])
            self.transfer_task['transfer_status'] = True
            self.clicker_manager.press_ecs()
            return




        path_task = {
            "food": "app\\windows\\shelter\\transfer\\img\\food.png",
            "wood": "app\\windows\\shelter\\transfer\\img\\wood.png",
            "steel": "app\\windows\\shelter\\transfer\\img\\steel.png",
            "oil": "app\\windows\\shelter\\transfer\\img\\oil.png",

        }
        path_task = resource_path(path_task[self.transfer_task['task']])
        coord_task = find_template_simple(path_task)
        if coord_task and not self.task_manager.stop_event.is_set():
            if not self.transfer_task['screen_status']:
                self.transfer_task['screen_status'] = True
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: WINDOW ID: %s SCREEN STATUS CHANGED TO %s",self.transfer_task['id'], self.transfer_task['screen_status'])
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: FIND TASK FRAME")
            self.clicker_manager.click(coord_task[0][0]+490, coord_task[0][1])
            time.sleep(1)
            self.clicker_manager.press_backspace(times=8)
            time.sleep(1)
            self.clicker_manager.input_numbers(numbers="9999999")
            time.sleep(1)
            path_vpered = resource_path(relative_path=self.locale.i10n('transfer-vpered'))
            coord_vpered = find_template_simple(path_vpered)
            if coord_vpered and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: FIND VPERED")
                self.clicker_manager.click(coord_vpered[0][0], coord_vpered[0][1])
                time.sleep(1)
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]:TRANSFER STARTED. GO TO STEP-3")
                self.transfer_step_3(window=window)
            else:
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]:BTN VPERED UNDEFIND")
                self.transfer_task['resourse_status'] = True
                logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: WINDOW ID: %s END RESOURSE. RESOURSE STATUS CHENGE TO TRUE", self.transfer_task['id'])
                self.clicker_manager.press_ecs()
        else:
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: TASK FRAME UNDEFIND")
            self.transfer_task['fail_count'] += 1
            logger.info("GAME OBJECT SERVICE: TRANSFER[STEP-4]: WINDOW ID: %s FAIL COUNT UP TO: %s", self.transfer_task['id'], self.transfer_task['fail_count'])
            self.clicker_manager.press_ecs()


# ============================ AUTORALLY ============================= #


    def check_autorally_icon(self, window):
        self.go_to_region()
        time.sleep(2)
        logger.info(msg="GAME OBJECT SERVICE: CHECK AUTORALLY GROUP")
        path_group_menu = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_menu.png")
        path_group_go_home = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_go_home.png")

        path_autorally_small1 = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\auto-rally-small-icon.png")
        path_autorally_small2 = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\auto-rally-small-icon2.png")

        path_autorally_small_list = [
            path_autorally_small1,
            path_autorally_small2
        ]

        path_autorally_big1 = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\auto-rally-big-icon.png")
        path_autorally_big2 = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\auto-rally-big-icon2.png")

        path_autorally_big_list = [
            path_autorally_big1,
            path_autorally_big2
        ]


        self.go_to_region()
        time.sleep(2)


        for path in path_autorally_small_list:
            coord = find_template_matches(path)
            if coord:
                logger.info(msg="GAME OBJECT SERVICE: AUTORALLY GROUP FIND")
                time.sleep(2)
                return True

        coord_group_menu = find_template_matches(path_group_menu)
        if coord_group_menu and not self.task_manager.stop_event.is_set():
            logger.info(msg="GAME OBJECT SERVICE: GO GROUP MENU")
            self.clicker_manager.click(coord_group_menu[0][0], coord_group_menu[0][1])
            time.sleep(3)
            self.clicker_manager.proportion_move_cursor_in_window(window=window.window, target_x=640, target_y=415)

            for i in range(3):
                for path in path_autorally_big_list:
                    coord = find_template_matches(path)
                    if coord:
                        logger.info(msg="AUTORALLY GROUP FIND")
                        self.clicker_manager.press_ecs()
                        time.sleep(2)
                        return True
                self.clicker_manager.scroll(target=-25)
                time.sleep(1)
            logger.info(msg="AUTORALLY GROUP UNDEFIND")
            self.clicker_manager.press_ecs()
            time.sleep(2)
            return False

        else:
            logger.info(msg="GAME OBJECT SERVICE: GROUP MENU UNDEFIND")
            logger.info(msg="GAME OBJECT SERVICE: AUTORALLY GROUP UNDEFIND")
            time.sleep(2)
            return False


    @check_stop_func
    def autorally_step_1(self, window, gather_trigger=False, gather_task=None):

        self.go_to_region()
        time.sleep(2)
        if gather_trigger == False:
            if self.check_autorally_icon(window=window):
                    return self.autorally_step_2(window=window)
            else:
                time.sleep(3)
                self.go_to_shelter()
                time.sleep(2)
                if not self.check_free_group():
                    self.back_all_group_home()
                    time.sleep(15)

        if gather_trigger == True:
            if has_time_passed(target_datetime=self.gather_task['rally_timer'], minutes=self.gather_task['rally_delay']):
                pass
            else:
                return

        self.go_to_ally()
        time.sleep(2)
        path_entry_rally = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\entry-rally.png")
        coord_entry_rally = find_template_matches(path_entry_rally, threshold=0.90)
        # Входим в меню сборов
        if coord_entry_rally and not self.task_manager.stop_event.is_set():
            logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY ALLIANCE RALLY MENU")
            self.clicker_manager.click(coord_entry_rally[0][0], coord_entry_rally[0][1])
            time.sleep(2)
            # Входим в меню автосбора
            path_autorally = resource_path(relative_path=self.locale.i10n('autorally-autosbor'))
            coord_autorally = find_template_matches(path_autorally, threshold=0.90)
            if coord_autorally and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY AUTORALLY MENU")
                self.clicker_manager.click(coord_autorally[0][0], coord_autorally[0][1])
                time.sleep(2)

                # Проверяем создан ли сбор
                path_autorally_cancel = resource_path(relative_path=self.locale.i10n('autorally-cancel'))
                coord_autorally_cancel = find_template_matches(path_autorally_cancel, threshold=0.90)
                if coord_autorally_cancel and not self.task_manager.stop_event.is_set():
                    logger.info("GAME OBJECT SERVICE: AUTORALLY: AUTORALLY ALREADY CREATE. GO TO ENTRY RALLY")
                else:
                    # Нажимаем создать автосбор
                    path_autorally_create = resource_path(relative_path=self.locale.i10n('autorally-create'))
                    coord_autorally_create = find_template_matches(path_autorally_create, threshold=0.90)
                    if coord_autorally_create and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: CREATE MENU")
                        self.clicker_manager.click(coord_autorally_create[0][0], coord_autorally_create[0][1])
                        time.sleep(2)
                        # Нажимаем сбор
                        path_autorally_sbor = resource_path(relative_path=self.locale.i10n('autorally-sbor'))
                        coord_autorally_sbor = find_template_matches(path_autorally_sbor, threshold=0.90)
                        if coord_autorally_sbor and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: AUTORALLY: CLICK SBOR MENU")
                            self.clicker_manager.click(coord_autorally_sbor[0][0], coord_autorally_sbor[0][1])
                            time.sleep(2)

                            # Нажимаем MAX
                            path_autorally_max = resource_path(relative_path=self.locale.i10n('autorally-max'))
                            coord_autorally_max = find_template_matches(path_autorally_max, threshold=0.90)
                            if coord_autorally_max and not self.task_manager.stop_event.is_set():
                                filter_max = filter_coordinates(coords=coord_autorally_max, threshold=10)
                                logger.info("GAME OBJECT SERVICE: AUTORALLY: CLICK MAX MENU")
                                for x,y in filter_max:
                                    self.clicker_manager.click(x, y)
                                    time.sleep(2)

                            # Нажимаем СОЗДАТЬ
                            path_autorally_sozdat = resource_path(relative_path=self.locale.i10n('autorally-start'))
                            coord_autorally_sozdat = find_template_matches(path_autorally_sozdat, threshold=0.90)
                            if coord_autorally_sozdat and not self.task_manager.stop_event.is_set():
                                logger.info("GAME OBJECT SERVICE: AUTORALLY: CLICK SOZDATb")
                                self.clicker_manager.click(coord_autorally_sozdat[0][0], coord_autorally_sozdat[0][1])
                                time.sleep(2)


                            path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
                            path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
                            # Проверяю появилось ли окно то что нет энергии
                            coord_green_use = find_template_matches(path_green_use)
                            if coord_green_use and not self.task_manager.stop_event.is_set():
                                logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: NO HAVE ENERGY")
                                green_count = 0
                                while not self.task_manager.stop_event.is_set():
                                    if green_count == 15:
                                        self.task_manager.stop_event.set()
                                        return
                                    coord_green_half = find_template_matches(path_green_half_empty)
                                    if coord_green_half and not self.task_manager.stop_event.is_set():
                                        coord_green_use_update = find_template_matches(path_green_use)
                                        filter_coord = filter_coordinates(coord_green_use_update)
                                        for x, y in filter_coord:
                                            self.clicker_manager.click(x, y)
                                            time.sleep(0.5)
                                        green_count += 1
                                    else:
                                        self.clicker_manager.press_ecs()
                                        time.sleep(2)
                                        self.clicker_manager.click(coord_autorally_sozdat[0][0], coord_autorally_sozdat[0][1])
                                        time.sleep(2)
                                        break
                        if gather_trigger == True:
                            self.gather_task['rally_timer'] = datetime.datetime.now()
                            logger.info("MULTIGATHER: [STEP-2] FIX new datetime %s", self.gather_task['rally_timer'])
                            self.gather_task['rally_delay'] = 30
                            logger.info("MULTIGATHER: [STEP-2] FIX new rally delay %s", self.gather_task['rally_delay'])
                        else:
                            logger.info("GAME OBJECT SERVICE: AUTORALLY: SBOR BUTTON UNDEFIND")
                    else:
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: CREATE MENU UNDEFIND")
                        self.go_to_region()
            else:
                logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY AUTORALLY MENU UNDEFIND")
        else:
            logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY ALLIANCE RALLY MENU UNDEFIND")
        self.go_to_shelter()
        time.sleep(2)
        self.go_to_region()
        time.sleep(2)
        if gather_trigger == False:
            self.autorally_step_2(window=window)
        else:
            return
    @check_stop_func
    def autorally_step_2(self, window):
        count_rally = 0
        while not self.task_manager.stop_event.is_set():
            if count_rally == 1:
                break
            count_rally += 1
            self.go_to_ally()
            time.sleep(2)
            path_entry_rally = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\entry-rally.png")
            coord_entry_rally = find_template_matches(path_entry_rally, threshold=0.90)
            # Входим в меню сборов
            if coord_entry_rally and not self.task_manager.stop_event.is_set():
                logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY ALLIANCE RALLY MENU")
                self.clicker_manager.click(coord_entry_rally[0][0], coord_entry_rally[0][1])
                time.sleep(2)
                ENRTY_STATUS = False
                for _ in range(10):
                    path_entry_plus = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\entry-rally-plus.png")
                    coord_entry_plus = find_template_matches(path_entry_plus, threshold=0.90)
                    if coord_entry_plus and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: ENTRY RALLY PLUS")
                        self.clicker_manager.click(coord_entry_plus[0][0], coord_entry_plus[0][1])
                        ENRTY_STATUS = True
                        time.sleep(5)
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: SLEEP 5")
                        break
                    self.clicker_manager.scroll(target=-25)
                    time.sleep(1)
                if ENRTY_STATUS:
                    path_entry_create_group = resource_path(relative_path=self.locale.i10n('entry-rally-create-group'))
                    coord_entry_create_group = find_template_matches(path_entry_create_group, threshold=0.90)
                    if coord_entry_create_group and not self.task_manager.stop_event.is_set():
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: CREATE GROUP")
                        self.clicker_manager.click(coord_entry_create_group[0][0], coord_entry_create_group[0][1])
                        time.sleep(2)
                        path_entry_marsh = resource_path(relative_path=self.locale.i10n('entry-rally-marsh'))
                        coord_entry_marsh = find_template_matches(path_entry_marsh, threshold=0.90)
                        if coord_entry_marsh and not self.task_manager.stop_event.is_set():
                            logger.info("GAME OBJECT SERVICE: AUTORALLY: MARSH")
                            self.clicker_manager.click(coord_entry_marsh[0][0], coord_entry_marsh[0][1])
                            time.sleep(2)
                            path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
                            path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
                                # Проверяю появилось ли окно то что нет энергии
                            coord_green_use = find_template_matches(path_green_use)
                            if coord_green_use and not self.task_manager.stop_event.is_set():
                                    logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: NO HAVE ENERGY")
                                    green_count = 0
                                    while not self.task_manager.stop_event.is_set():
                                        if green_count == 15:
                                            self.task_manager.stop_event.set()
                                            return
                                        coord_green_half = find_template_matches(path_green_half_empty)
                                        if coord_green_half and not self.task_manager.stop_event.is_set():
                                            coord_green_use_update = find_template_matches(path_green_use)
                                            filter_coord = filter_coordinates(coord_green_use_update)
                                            for x, y in filter_coord:
                                                self.clicker_manager.click(x, y)
                                                time.sleep(0.5)
                                            green_count += 1
                                        else:
                                            self.clicker_manager.press_ecs()
                                            time.sleep(2)
                                            self.clicker_manager.click(coord_entry_marsh[0][0], coord_entry_marsh[0][1])
                                            time.sleep(2)
                                            logger.info("GAME OBJECT SERVICE: RALLY[STEP-9]: ENTRY IS SUCCESFULL. RESTART ENTRY RALLY")
                                            break
                            # Не нашел МАРШ
                        else:
                            logger.info("GAME OBJECT SERVICE: AUTORALLY: MARSH UNDEFIND. RESTART ENTRY RALLY")
                            continue

                        # Не нашел создать отряд
                    else:
                        logger.info("GAME OBJECT SERVICE: AUTORALLY: CREATE GROUP UNDEFIND.")
                        time.sleep(2)
                        continue
                    # Не нашел плюс
                else:
                    logger.info("GAME OBJECT SERVICE: AUTORALLY: PLUS UNDEFIND.")
                    time.sleep(2)
                    continue



# =============================== GATHER ================================= #

    def choose_param_gather(self, task):
        self.choose_window: tk.Toplevel = tk.Toplevel()

        window_width = 300
        window_height = 200

        screen_width = self.choose_window.winfo_screenwidth()
        screen_height = self.choose_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.choose_window.title = self.locale.i10n('gather-choose-param-title')
        self.choose_window.geometry(f"{215}x{180}+{x}+{y}")
        self.choose_window.resizable(width=False, height=False)
        self.choose_window.overrideredirect(boolean=True)

        for i in range(5):
            self.choose_window.columnconfigure(i, weight=1, uniform="cols")  # uniform для одинаковой ширины
        for i in range(6):
            self.choose_window.rowconfigure(i, weight=1)


        self.btn_start = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-start'), command=lambda: self.get_data(task=task))
        self.btn_cancel = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-cancel'), command=lambda: self.choose_window.destroy())
        lbl_terry_alliance = tk.Label(master=self.choose_window, text=self.locale.i10n('gather-choose-param-terry-ally'), justify='center', anchor='center')
        self.path_food_img = resource_path("app\\windows\\shelter\\gather\\img\\food.png")
        self.img_food = tk.PhotoImage(file=self.path_food_img)
        self.path_wood_img = resource_path("app\\windows\\shelter\\gather\\img\\wood.png")
        self.img_wood = tk.PhotoImage(file=self.path_wood_img)
        self.path_steel_img = resource_path("app\\windows\\shelter\\gather\\img\\steel.png")
        self.img_steel = tk.PhotoImage(file=self.path_steel_img)
        self.path_oil_img = resource_path("app\\windows\\shelter\\gather\\img\\oil.png")
        self.img_oil = tk.PhotoImage(file=self.path_oil_img)
        self.path_all_gather_img = resource_path("app\\windows\\shelter\\gather\\img\\all_gather.png")
        self.img_all_gather = tk.PhotoImage(file=self.path_all_gather_img)


        lbl_food = tk.Label(master=self.choose_window, image=self.img_food)
        lbl_wood = tk.Label(master=self.choose_window, image=self.img_wood)
        lbl_steel = tk.Label(master=self.choose_window, image=self.img_steel)
        lbl_oil = tk.Label(master=self.choose_window, image=self.img_oil)
        lbl_all_gather = tk.Label(master=self.choose_window, image=self.img_all_gather)

        self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
        self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")

        self.var_food = tk.BooleanVar()
        self.var_wood = tk.BooleanVar()
        self.var_steel = tk.BooleanVar()
        self.var_oil = tk.BooleanVar()
        self.var_all_gather = tk.BooleanVar()
        self.var_terry_alliance = tk.BooleanVar()

        self.img_select = tk.PhotoImage(file=self.path_select_img)
        self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

        self.chckbtn_food = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_food,
                                          borderwidth=0)
        self.chckbtn_wood = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_wood,
                                          borderwidth=0)
        self.chckbtn_steel = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_steel,
                                          borderwidth=0)
        self.chckbtn_oil = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_oil,
                                          borderwidth=0)
        self.chckbtn_all_gather = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_all_gather,
                                          borderwidth=0,
                                          command=self.update_all_chckbox
                                        )
        self.chckbtn_terry_alliance = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_terry_alliance,
                                          borderwidth=0)

        lbl_food.grid(row=1, column=0, padx=1, sticky=EW)
        lbl_wood.grid(row=1, column=1, padx=1, sticky=EW)
        lbl_steel.grid(row=1, column=2, padx=1, sticky=EW)
        lbl_oil.grid(row=1,column=3, padx=1, sticky=EW)
        lbl_all_gather.grid(row=1, column=4, padx=1, sticky=EW)


        self.chckbtn_food.grid(row=2,column=0, padx=1, sticky=EW)
        self.chckbtn_wood.grid(row=2,column=1, padx=1, sticky=EW)
        self.chckbtn_steel.grid(row=2,column=2, padx=1, sticky=EW)
        self.chckbtn_oil.grid(row=2,column=3, padx=1, sticky=EW)
        self.chckbtn_all_gather.grid(row=2,column=4, padx=1, sticky=EW)


        lbl_terry_alliance.grid(row=3, column=0, columnspan=5, sticky=EW)
        self.chckbtn_terry_alliance.grid(row=4,column=0, columnspan=5, sticky=EW)

        self.btn_start.grid(row=5,column=0, columnspan=2, padx=5, pady=1)
        self.btn_cancel.grid(row=5,column=3, columnspan=2, padx=5, pady=1)

    def update_all_chckbox(self):
        if self.var_all_gather.get():
            self.var_food.set(value=True)
            self.var_wood.set(value=True)
            self.var_steel.set(value=True)
            self.var_oil.set(value=True)
        else:
            self.var_food.set(value=False)
            self.var_wood.set(value=False)
            self.var_steel.set(value=False)
            self.var_oil.set(value=False)


    def get_data(self, task):
        data = {
            "food": self.var_food.get(),
            "wood": self.var_wood.get(),
            "steel": self.var_steel.get(),
            "oil": self.var_oil.get(),

            }
        temp_list = []
        for k,v in data.items():
            if v:
                temp_list.append(k)
        self.gather_data = {
            "task_list": temp_list,
            "ally_triger": self.var_terry_alliance.get()
            }
        self.choose_window.destroy()
        logger.info(msg=f"GATHER: GET DATA TASK:[{self.gather_data['task_list']}] ALLIANCE TERRITORY: [{self.gather_data['ally_triger']}]")
        if temp_list:
        # МЕСТО ЗАПУСКА THREAD
            self.task_manager.start_task(task_func=lambda: self.gather_algorithm(task=task, data=self.gather_data), on_complete_func=self.gather_end, name_service="MultiGather Service")

            logger.info(msg=f"GATHER: RUNNING")
        else:
            messagebox.showwarning(title=self.locale.i10n('gather-task-messagewarning-title'), message=self.locale.i10n('gather-task-messagewarning-message'))

    def gather_end(self):
        pass

    def gather_algorithm(self, data, task):
        self.gather_object_list = []
        self.gather_task_data = {}

        self.windows_manager.init_multi_windows()
        self.windows_index = 0

        for id, window in enumerate(self.windows_manager.windows_list, start=1):
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                self.gather_task_data = {
                    "id": id,
                    "window": window,
                    "screen_status": None,
                    "hide_discount": False,
                    'task': None,
                    "additional_event_task": task,
                    "rally_delay": 3,
                    "rally_timer": None,
                    "fail_task": False,
                    "lvl_down_task": False,
                    "failed_count": 0,
                    "pause_mission_time": None,
                    'ally_donation_time': None,
                    'get_lvl': 0,
                    'stat': {}
                    }
                self.gather_task_data.update(data)
                self.gather_object_list.append(self.gather_task_data)
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="TRANSFER: WINDOW MOVED TO [10,10].")
            else:
                break


        while not self.task_manager.stop_event.is_set():
            self.task_manager.app.validator.get_time()
            if not self.windows_manager.windows_list:
                break
            if self.windows_index > len(self.gather_object_list)-1:
                logger.info(msg="GATHER: ALL WINDOWS GATHERED. DROP INDEX WINDOW.")
                self.windows_index = 0
            window: Window = self.gather_object_list[self.windows_index]['window']
            self.gather_task = self.gather_object_list[self.windows_index]

            time.sleep(2)
            try:
                window.window.activate()
                time.sleep(3)

                self.gather_step_1(window=window)


                if self.gather_task['additional_event_task'] == 'hunt':
                    self.hunt_afk_algorithm(window=window)

                if self.gather_task['additional_event_task'] == 'autorally':
                    self.autorally_step_1(window=window, gather_trigger=True, gather_task=self.gather_task)


            except PyGetWindowException as error:
                print("error open windows")


            self.windows_index += 1
        text=self.locale.i10n('gather-task-messageinfo-message')+"\n"
        for gather, value in self.gather_stat.items():
            text += self.locale.i10n(message_id='gather-stats-entry',resource=gather, gathered=value['count_gather'], tasks=value['count_task'])
            text += "\n"
        messagebox.showinfo(title="Gather Task", message=text)

    def check_region_screen(self) -> bool:
        logger.info(msg=f"GATHER: CHECK REGION FUNC")
        path_region_btn = resource_path(relative_path="app\\img\\game_button\\go-region.png")
        coord_region = find_template_matches(path_region_btn)
        if coord_region:
            logger.info(msg=f"GATHER: REGION IN ACTION")
            return True
        logger.info(msg=f"GATHER: SHELTER IN ACTION")
        return False


    @check_stop_func
    def gather_step_1(self, window: Window):
        # Проверка в регионе ли
        if self.check_region_screen():
            logger.info(msg="GATHER: [STEP-1] REGION DETECTED. GO TO STEP-2")
            if not self.gather_task['hide_discount']:
                self.hide_discont()
                time.sleep(2)
                self.gather_task['hide_discount'] = True
                self.go_to_region()
            time.sleep(2)
            return self.gather_step_2(window=window)

        else:
            logger.info(msg="GATHER: [STEP-1] REGION DON'T DETECTED - BACK IN STEP-1")
            self.go_to_region()
            time.sleep(3)
            return self.gather_step_1(window=window)

    @check_stop_func
    def pause_gather(self, window):
        self.click_hand()
        time.sleep(2)
        if has_time_passed(target_datetime=self.gather_task['ally_donation_time'], minutes=180):
            self.take_ally_technology_bonus(window=window)
            self.gather_task['ally_donation_time'] = datetime.datetime.now()
            time.sleep(1)
        self.hide_discont()
        time.sleep(1)
        self.go_to_shelter()
        time.sleep(2)
        self.buff_gather()
        time.sleep(2)
        self.buff_resourse()
        time.sleep(2)
        self.take_cex(window=window)
        time.sleep(2)
        self.take_ferm()
        time.sleep(5)
        self.take_shop()
        time.sleep(1)
        self.take_police_dron(window=window)
        time.sleep(2)
        self.police_poisk()
        time.sleep(2)
        self.take_racia()
        time.sleep(2)
        self.click_hand()
        time.sleep(2)





    @check_stop_func
    def gather_step_2(self, window: Window):
        # Проверяем какой дополнительный ивент выполняем
        if self.gather_task['additional_event_task'] == "gather" or self.gather_task['additional_event_task'] == "hunt":
            logger.info("GATHER: [STEP-2] Additional event is %s", self.gather_task['additional_event_task'])

            # Проверка на наличие свободных отрядов
            self.go_to_shelter()
            time.sleep(2)
            if self.check_free_group():
                logger.info(msg="GATHER: [STEP-2] FREE TROOPS. - CLICK TO 'POISK' ")
                time.sleep(1)
                self.go_to_region()
                time.sleep(2)
                # Клик по поиску
                path_loup = resource_path(relative_path="app\\img\\game_button\\loup.png")
                coord_loup = find_template_matches(path_loup)
                if coord_loup:
                    self.clicker_manager.click(coord_loup[0][0], coord_loup[0][1])
                    time.sleep(2)


                # self.clicker_manager.proportion_click_in_window(window=window.window, target_x=45, target_y=480)
                time.sleep(2)
                logger.info(msg="GATHER: [STEP-2] GO TO STEP-3 ")
                return self.gather_step_3(window=window)
            else:
                logger.info(msg="GATHER: [STEP-2] ALL TROOPS USED")
                self.gather_task['task'] = None
                self.gather_task['lvl_down_task'] = False
                if self.gather_task['failed_count'] != 0:
                    self.gather_task['failed_count'] = 0
                    logger.info(msg=f"GATHER: [STEP-2] FAILED COUNT DROP TO 0")
                # if has_time_passed(target_datetime=self.gather_task['pause_mission_time'], minutes=60):
                #     logger.info(msg="GATHER: [STEP-2] JOIN PAUSE MISSION TASK")
                #     self.pause_gather(window=window)
                #     self.gather_task['pause_mission_time'] = datetime.datetime.now()
                #     logger.info("GATHER: [STEP-2] FIX new pause mission time %s", self.gather_task['pause_mission_time'])
                #     time.sleep(2)
                else:
                    logger.info(msg="GATHER: [STEP-2] PAUSE MISSION TASK TIME NOT PREPARE")
                logger.info("GATHER: [STEP-2] SLEEP 30 SEC. OUT GATHER")
                time.sleep(30)
                return

        if self.gather_task['additional_event_task'] == "autorally":
            logger.info("GATHER: [STEP-2] Additional event is %s", self.gather_task['additional_event_task'])


            logger.info("GATHER: [STEP-2] CHECK TIMER RALLY")
            # проверяем прошло ли 30 минут после создания ралли.
            if has_time_passed(self.gather_task['rally_timer'], self.gather_task['rally_delay']):
                logger.info("GATHER: [STEP-2] TIMER RALLY IS TRUE")
                # Т.к прошло 30 минут, уходим проверять создано ли ралли
                # Тут оказалось что ралли еще создано
                logger.info("GATHER: [STEP-2] CHECK AUTORALLY ICON")
                if self.check_autorally_icon(window=window):
                    logger.info("GATHER: [STEP-2] CHECK AUTORALLY ICON IS TRUE")
                    self.gather_task['rally_timer'] = datetime.datetime.now()
                    logger.info("GATHER: [STEP-2] FIX new datetime %s", self.gather_task['rally_timer'])
                    self.gather_task['rally_delay'] = 15
                    logger.info("GATHER: [STEP-2] FIX new rally delay %s", self.gather_task['rally_delay'])
                    time.sleep(2)
                    self.go_to_shelter()
                    time.sleep(2)
                    if self.check_free_group():
                        logger.info(msg="GATHER: [STEP-2] FREE TROOPS. - CLICK TO 'POISK' ")
                        time.sleep(1)
                        self.go_to_region()
                        # Клик по поиску
                        time.sleep(2)
                        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=45, target_y=480)
                        time.sleep(2)
                        logger.info(msg="GATHER: [STEP-2] GO TO STEP-3 ")
                        return self.gather_step_3(window=window)
                    else:
                        logger.info(msg="GATHER: [STEP-2] ALL TROOPS USED")
                        self.gather_task['task'] = None
                        self.gather_task['lvl_down_task'] = False
                        if self.gather_task['failed_count'] != 0:
                            self.gather_task['failed_count'] = 0
                            logger.info(msg=f"GATHER: [STEP-2] FAILED COUNT DROP TO 0")
                        if has_time_passed(target_datetime=self.gather_task['pause_mission_time'], minutes=60):
                            logger.info(msg="GATHER: [STEP-2] JOIN PAUSE MISSION TASK")
                            self.pause_gather(window=window)
                            self.gather_task['pause_mission_time'] = datetime.datetime.now()
                            logger.info("GATHER: [STEP-2] FIX new pause mission time %s", self.gather_task['pause_mission_time'])
                            time.sleep(2)
                        else:
                            logger.info(msg="GATHER: [STEP-2] PAUSE MISSION TASK TIME NOT PREPARE")
                        logger.info("GATHER: [STEP-2] SLEEP 30 SEC. OUT GATHER")
                        time.sleep(30)
                        return
                # ТУТ Обнаружили что 30 мин прошло и ралли не создано
                else:
                    logger.info("GATHER: [STEP-2] CHECK AUTORALLY ICON IS FALSE. GO TO CREATE RALLY")
                    time.sleep(2)
                    self.go_to_shelter()
                    time.sleep(2)
                    # Тут прошло 30 минут. И Ралли уже нет. Проверяю есть ли свободный отряд.
                    if self.check_free_group():
                        #  Уходим создавать ралли.
                        self.go_to_region()
                        time.sleep(2)
                        return
                    else:
                        # Возвращаю первый отряд домой
                        self.back_first_group_home()
                        # Засыпаю на 30 сек чтобы дождаться пока отряд дойдет в убежку
                        logger.info("GATHER: [STEP-2] WAIT 45 SEC BACK TROOPS TO HOME")
                        time.sleep(45)
                        return
            # Тут 30 мин. не прошло. Уходим копать.
            else:
                logger.info("GATHER: [STEP-2] TIMER RALLY IS FALSE")
                time.sleep(2)
                self.go_to_shelter()
                time.sleep(2)
                if self.check_free_group():
                    logger.info(msg="GATHER: [STEP-2] FREE TROOPS. - CLICK TO 'POISK' ")
                    time.sleep(1)
                    self.go_to_region()
                    time.sleep(2)
                    # Клик по поиску
                    self.clicker_manager.proportion_click_in_window(window=window.window, target_x=45, target_y=480)
                    time.sleep(2)
                    logger.info(msg="GATHER: [STEP-2] GO TO STEP-3 ")
                    return self.gather_step_3(window=window)
                else:
                    logger.info(msg="GATHER: [STEP-2] ALL TROOPS USED")
                    self.gather_task['task'] = None
                    self.gather_task['lvl_down_task'] = False
                    if self.gather_task['failed_count'] != 0:
                        self.gather_task['failed_count'] = 0
                        logger.info(msg=f"GATHER: [STEP-2] FAILED COUNT DROP TO 0")
                    if has_time_passed(target_datetime=self.gather_task['pause_mission_time'], minutes=60):
                        logger.info(msg="GATHER: [STEP-2] JOIN PAUSE MISSION TASK")
                        self.pause_gather(window=window)
                        self.gather_task['pause_mission_time'] = datetime.datetime.now()
                        logger.info("GATHER: [STEP-2] FIX new pause mission time %s", self.gather_task['pause_mission_time'])
                        time.sleep(2)
                    else:
                        logger.info(msg="GATHER: [STEP-2] PAUSE MISSION TASK TIME NOT PREPARE")
                    logger.info("GATHER: [STEP-2] SLEEP 30 SEC. OUT GATHER")
                    time.sleep(30)
                    return

    def click_on_gather_task(self, task, window):

        logger.info(msg="GATHER: CLICK ON TASK RESOURCE FUNC")
        if task == 'food':
        # 655 645
            self.clicker_manager.proportion_click_in_window(
                window=window.window,
                target_x=655,
                target_y=645
                )
            logger.info(msg="GATHER: CLICK FOOD")
        elif task == "wood":
        # 805 645
            self.clicker_manager.proportion_click_in_window(
                window=window.window,
                target_x=805,
                target_y=645
                )
            logger.info(msg="GATHER: CLICK WOOD")
        elif task == "steel":
        # 945 645
            self.clicker_manager.proportion_click_in_window(
                window=window.window,
                target_x=945,
                target_y=645
                )
            logger.info(msg="GATHER: CLICK STEEL")

        elif task == "oil":
        #  1085 645
            self.clicker_manager.proportion_click_in_window(
                window=window.window,
                target_x=1085,
                target_y=645
                )
            logger.info(msg="GATHER: CLICK OIL")

    @check_stop_func
    def gather_step_3(self, window: Window):

        # Проверяю не включен ли тригер, что в задании пошло что-то не то
        ### Причины:
        #### Не нашел шаг понижения уровня в STEP-4
        #### failcount == 3 а значит в следующий круг нужно сбрость задание чтобы он в икле не продолжил стучаться в один ресурс

        if self.gather_task['fail_task']:
            self.gather_task['task'] = None
            self.gather_task['fail_task'] = False

        if self.gather_task['failed_count'] == 3:
            self.gather_task['fail_task'] = True
            self.gather_task['task'] = random.choice(['food','wood', 'steel', 'oil'])
            logger.info(msg=f"GATHER: [STEP-3] FAILED COUNT MORE 5 - GET ANOTHER TASK {self.gather_task['task']}")
            self.gather_task['failed_count'] = 0
            logger.info(msg=f"GATHER: [STEP-3] FAILED COUNT DROP TO 0")

        if self.gather_task['task'] is None:
            self.gather_task['task'] = random.choice(self.gather_data['task_list'])
            logger.info(msg=f"GATHER: [STEP-3] GET RANDOM TASK - {self.gather_task['task']}")

        logger.info(msg=f"GATHER: [STEP-3] TASK: {self.gather_task['task']}")
        time.sleep(1)
        self.click_on_gather_task(task=self.gather_task['task'], window=window)
        time.sleep(2)
        if self.gather_task['lvl_down_task']:
            logger.info(msg="GATHER: [STEP-3] GO TO STEP-4 [TASK LVL DOWN TRIGGER - TRUE]")
            return self.gather_step_4(window=window, lvl="down")
        else:
            logger.info(msg="GATHER: [STEP-3] GO TO STEP-4 [TASK LVL DOWN TRIGGER - FALSE]")
            return self.gather_step_4(window=window)

    def check_max_lvl_gather(self):
        logger.info(msg="GATHER: CHECK MAX_LVL RESOURCE FUNC")
        path = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl_max.png")
        get_max_lvl = find_template_matches_color(path, threshold=0.9)
        if get_max_lvl:
            logger.info(msg="GATHER: RESOURCE MAX_LVL")
            return True
        logger.info(msg="GATHER: RESOURCE NOT MAX_LVL")
        return False


    @check_stop_func
    def gather_step_4(self, window: Window, lvl = None):
        if lvl is None:
            # Проверяю кнопка повысить уровень доступна ли
            if self.check_max_lvl_gather():
                logger.info(msg="GATHER: [STEP-4] LVL RESOURCE MAX. GO TO STEP-5]")
                self.gather_task['get_lvl'] = 6
                return self.gather_step_5(window)
            else:
                # Начинаю в цикле подымать уровень до максимального
                path_lvl_up = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvlup.png")
                count_up = 0
                while not self.task_manager.stop_event.is_set():
                    # Проверяю не больше ли 7 раз он нажал
                    if count_up > 8:
                        return self.gather_step_1(window=window)
                    time.sleep(0.5)
                    coord_lvl_up = find_template_matches(path_lvl_up)
                    if coord_lvl_up and not self.task_manager.stop_event.is_set():
                        self.clicker_manager.click(coord_lvl_up[0][0], coord_lvl_up[0][1])
                        logger.info(msg="GATHER: [STEP-4] CLICK PLUS")
                    else:
                        logger.error(msg="GATHER: [STEP-4] COORD BUTTON PLUS NO DEFINED")
                    time.sleep(0.5)
                    if self.check_max_lvl_gather():
                        logger.info(msg="GATHER: [STEP-4] RESOURCE LEVEL MAX")
                        break
                    else:
                        count_up += 1
                        logger.info("GATHER: [STEP-4] GATHER NOT MAX. COUNT UP +1: %s", count_up)


                path_lvl_gather= {
                        1: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl1.png"),
                        2: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl2.png"),
                        3: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl3.png"),
                        4: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl4.png"),
                        5: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl5.png"),
                        6: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl6.png")
                }

                current_lvl = 0
                for lvl, path in path_lvl_gather.items():
                    time.sleep(0.5)
                    if self.task_manager.stop_event.is_set():
                        break
                    coord_lvl = find_template_matches(path, threshold=0.95)
                    if coord_lvl:
                        logger.info("GATHER: [STEP-4] GET CURRENT LVL: %s", lvl)
                        current_lvl = lvl
                        self.gather_task['get_lvl'] = lvl
                        break

                if current_lvl == 0:
                    logger.info("GATHER: [STEP-4] FAILED GET CURRENT LVL. GO TO STEP - 1")
                    return self.gather_step_1(window=window)

                logger.info(msg="GATHER: [STEP-4] GO TO STEP-5")
                return self.gather_step_5(window)
        # Включен режим понижения. Т.к в предыдущий раз не нашли ресурс нужного уровня
        elif lvl == "down":
            path_lvl_down = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvldown_gather.png")
            coord_lvl_down = find_template_matches(path_lvl_down)
            time.sleep(0.5)
            # Проверяю нашел ли кнопку минус (понизить уровень)
            if coord_lvl_down:
                self.clicker_manager.click(coord_lvl_down[0][0], coord_lvl_down[0][1])
                logger.info(msg="GATHER: [STEP-4] CLICK MINUS")
                time.sleep(0.5)
                logger.info(msg="GATHER: [STEP-4] TASK LVL DOWN COMPLETED - LVL_DOWN_TRIGGER CHANGE TO False")
                # После успешного нажатия на кнопку минус, отключаю Тригер понижения уровня
                self.gather_task['lvl_down_task'] = False
                logger.info(msg="GATHER: [STEP-4] GO TO STEP-5")
                return self.gather_step_5(window)
            else:
                # Проверяю, не минимальный ли уже уровень. Ищу кнопку минус серую
                path_lvl_min = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvlmin.png")
                coord_lvl_min = find_template_matches(path_lvl_min)
                if coord_lvl_min:
                    logger.info(msg="GATHER: [STEP-4] CLICK MINUS IN MINIMUM")
                    logger.info(msg="GATHER: [STEP-4] TASK LVL DOWN COMPLETED - LVL_DOWN_TRIGGER CHANGE TO False")
                    # Отключаю тригер понижения уровня т.к уже достингут минимальный уровень, пусть ищет сначала.
                    self.gather_task['lvl_down_task'] = False
                    logger.info(msg="GATHER: [STEP-4] GO TO STEP-5")
                    path_lvl_gather= {
                            1: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl1.png"),
                            2: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl2.png"),
                            3: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl3.png"),
                            4: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl4.png"),
                            5: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl5.png"),
                            6: resource_path(relative_path="app\\windows\\shelter\\gather\\img\\lvl6.png")
                    }

                    current_lvl = 0
                    for lvl, path in path_lvl_gather.items():
                        time.sleep(0.5)
                        if self.task_manager.stop_event.is_set():
                            break
                        coord_lvl = find_template_matches(path, threshold=0.95)
                        if coord_lvl:
                            logger.info("GATHER: [STEP-4] GET CURRENT LVL: %s", lvl)
                            current_lvl = lvl
                            break

                    if current_lvl == 0:
                        logger.info("GATHER: [STEP-4] FAILED GET CURRENT LVL. GO TO STEP - 1")
                        return self.gather_step_1(window=window)

                    return self.gather_step_5(window)

                else:
                    # Тут пошло что-то не так, бот не нашел кнопку минимальную кнопку минуса и сами минс не нашел
                    logger.info(msg="GATHER: [STEP-4] TASK LVL DOWN FAILED - LVL_DOWN_TRIGGER CHANGE TO False")
                    # Поэтому сбрасывают триггер понижения уровня
                    self.gather_task['lvl_down_task'] = False
                    # Повышаю счётчик ошибки задания для данного ресурса
                    self.gather_task['failed_count'] += 1
                    logger.info(msg="GATHER: [STEP-4] CLICK MINUS NOT DEFIEND. TASK IS FAILED GO TO STEP 1")
                    time.sleep(2)
                    return self.gather_step_1(window=window)


    @check_stop_func
    def gather_step_5(self, window: Window):
         # Нажатие на поиск
        path_poisk = resource_path(relative_path=self.locale.i10n('gather-poisk'))
        coord_poisk = find_template_matches(path_poisk)
        time.sleep(2)
        # Ищу кнопку поиск
        if coord_poisk:
            logger.info(msg="GATHER: [STEP-5] CLICK TO YELLOW BUTTON - POISK")
            self.clicker_manager.click(coord_poisk[0][0], coord_poisk[0][1])
            time.sleep(2)
        else:
            logger.error(msg="GATHER: [STEP-5] COORD YELLOW BUTTON - POISK NO DEFINED. GO TO STEP 1")
            self.gather_task['failed_count'] += 1
            self.go_to_region()
            return self.gather_step_1(window=window)

        logger.info(msg="GATHER: [STEP-5] GO TO STEP-6")
        return self.gather_step_6(window=window)

    @check_stop_func
    def gather_step_6(self, window: Window):
        # Нажатие по ресурсу просто в центр экрана
        # 640 390
        time.sleep(1)
        logger.info(msg="GATHER: [STEP-6] CLICK TO RESOURCE")
        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=640, target_y=390)
        time.sleep(4)
        logger.info(msg="GATHER: [STEP-6] GO TO STEP-7")
        return self.gather_step_7(window)

    @check_stop_func
    def gather_step_7(self, window: Window):
        path_gather = resource_path(relative_path=self.locale.i10n('gather-button'))
        coord_gather = find_template_matches(path_gather)
        time.sleep(2)
        # Ищу кнопку СОБРАТЬ
        if coord_gather:
            logger.info(msg="GATHER: [STEP-7] BUTTON GATHER IN SCREEN")
            logger.info(msg=f"GATHER: [STEP-7] TRIGGER ALLY TERRITORY - {self.gather_task['ally_triger']}")

            # ПРОВЕРКА ТРИГЕРА - СОБИРАТЬ ЛИ НА ТЕРРИТОРИИ АЛЬНЯСА
            if self.gather_task['ally_triger']:
                path_alliance_terry = resource_path(relative_path="app\\windows\\shelter\\gather\\img\\30.png")
                coord_alliance_terry = find_template_matches(path_alliance_terry)
                # Ищу показатель что ресурс на территории альянса
                if coord_alliance_terry:
                    logger.info(msg="GATHER: [STEP-7] RESOURCE IN ALLY TERRITORY - CLICK TO GATHER BUTTON")
                    self.clicker_manager.click(coord_gather[0][0], coord_gather[0][1])
                    time.sleep(4)
                    logger.info(msg="GATHER: [STEP-7] GO TO STEP-8")
                    return self.gather_step_8(window=window)
                else:
                    # Ресурс не на территории Альянса
                    logger.info(msg="GATHER: [STEP-7] RESOURCE NOT IN ALLY TERRITORY - CLICK TO SHELTER")
                    self.clicker_manager.proportion_click_in_window(window=window.window, target_x=70, target_y=680)
                    time.sleep(4)
                    # Неудачная попытка найти ресурс, он оказался не на территории альянса.
                    # Повышаю счётчик неудачных попыток
                    self.gather_task['failed_count'] += 1
                    logger.info(msg=f"GATHER: [STEP-7] FAILED COUNT UP TO 1. COUNT: [{self.gather_task['failed_count']}]")
                    # Попробую найти тот же ресурс, но уровнем ниже
                    self.gather_task['lvl_down_task'] = True
                    logger.info(msg="GATHER: [STEP-7] GO TO STEP-1")
                    return self.gather_step_1(window=window)

            # ТРИГГЕР АЛЬЯНСА - False
            else:
                # ТУТ нам не важно где ресурс находится, мы его берем копать
                time.sleep(1)
                logger.info(msg="GATHER: [STEP-7] CLICK TO GATHER BUTTON")
                self.clicker_manager.click(coord_gather[0][0], coord_gather[0][1])
                time.sleep(4)
                logger.info(msg="GATHER: [STEP-7] GO TO STEP-8")
                return self.gather_step_8(window=window)

        # ТУТ ОН НЕ НАШЕЛ КНОПКУ СОБИРАТЬ
        else:
            logger.info(msg="GATHER: [STEP-7] BUTTON GATHER NO DEFINED")
            # Повышаю счётчик неудачных попыток выполнения задания
            self.gather_task['failed_count'] += 1
            # Попробую выполнить задание с уровнем ниже
            self.gather_task['lvl_down_task'] = True
            logger.info(msg=f"GATHER: [STEP-7] LVL DOWN TASK CHANGED TO - {self.gather_task['lvl_down_task']}")
            logger.info(msg=f"GATHER: [STEP-7] FAILED COUNT UP TO 1. COUNT: [{self.gather_task['failed_count']}]")
            time.sleep(1)
            logger.info(msg="GATHER: [STEP-7] GO TO STEP-2")
            return self.gather_step_1(window=window)


    def back_in_main_screen(self):
        # НЕАКТУАЛЬНО
        time.sleep(2)
        logger.info(f"GATHER: CLICK - CONTROL MAIN SCREEN")
        path_region = resource_path(relative_path="app\\img\\game_button\\go-region.png")
        path_shelter = resource_path(relative_path="app\\img\\game_button\\go-shelter.png")

        while not self.task_manager.stop_event.is_set():
            coord_region = find_template_matches(path_region)
            time.sleep(1)
            if coord_region:
                logger.info(f"GATHER:: REGION IN ACTION")
                break
            coord_shelter = find_template_matches(path_shelter)
            time.sleep(1)
            if coord_shelter:
                logger.info(f"GATHER: SHELTER IN ACTION")
                break

            self.clicker_manager.press_ecs()
            time.sleep(6)

    @check_stop_func
    def gather_step_8(self, window: Window):
        # Создать отряд
        # 970 275
         # Нажатие на создать отряд
        path_create_group = resource_path(relative_path=self.locale.i10n('gather-create-group'))
        coord_create_group = find_template_matches(path_create_group)
        time.sleep(2)
        # Ищу кнопку Создать отряд
        if coord_create_group:
            logger.info(msg="GATHER: [STEP-8] CLICK TO YELLOW BUTTON - CREATE GROUP")
            self.clicker_manager.click(coord_create_group[0][0], coord_create_group[0][1])
            time.sleep(5)
            logger.info(msg="GATHER: [STEP-8] GO TO STEP-9")
            return self.gather_step_9(window=window)

        # ТУТ ОН НЕ НАШЕЛ КНОПКУ СОЗДАТЬ ОТРЯД ПОТОМУ ЧТО ВСЕ ОТРЯДЫ ЗАНЯТЫ
        else:

            logger.info(msg="GATHER: [STEP-8 COORD YELLOW BUTTON - CREATE GROUP NO DEFINED. ALL TROOPS IS BUSY")
            time.sleep(3)
            # нажимаю на пустое место чтобы выйти в регион
            self.clicker_manager.proportion_click_in_window(window=window.window, target_x=640, target_y=390)
            time.sleep(2)
            self.clicker_manager.back_in_main_screen(task_manager=self.task_manager)
            # В идеале нужно выйти из последовательности и передать управление другой программе
            # self.windows_index += 1
            logger.info(msg="GATHER: [STEP-8] GATHER TASK CAN NOT TO BE COMLETED, DROP TASK")
            self.gather_task['task'] = None
            if self.gather_task['failed_count'] != 0:
                self.gather_task['failed_count'] = 0
                logger.info(msg=f"GATHER: [STEP-8] FAILED COUNT DROP TO 0")
            if self.gather_task['lvl_down_task'] == True:
                self.gather_task['lvl_down_task'] = False
                logger.info(msg=f"GATHER: [STEP-8] LVL DOWN TASK CHANGED TO - {self.gather_task['lvl_down_task']}")

            # Запускаем цикл на следующий отряд если нет другого задания
            if self.gather_task['additional_event_task']  == "gather" or self.gather_task['additional_event_task'] == "hunt" or self.gather_task['additional_event_task'] == "autorally":
                logger.info("GATHER: [STEP-8] Additional event is %s. Go to next troops", self.gather_task['additional_event_task'])
                # Запускаем цикл на следующий отряд
                return self.gather_step_1(window=window)


    @check_stop_func
    def gather_step_9(self, window: Window):

        resourse_data = {
            "food": {
                1:240000,
                2:480000,
                3:960000,
                4:1440000,
                5:1920000,
                6:2400000
                     },
            "wood": {
                1:240000,
                2:480000,
                3:960000,
                4:1440000,
                5:1920000,
                6:2400000
                     },
            "steel": {
                1:240000,
                2:480000,
                3:960000,
                4:1440000,
                5:1920000,
                6:2400000
                },
            "oil": {
                1:240000,
                2:480000,
                3:960000,
                4:1440000,
                5:1920000,
                6:2400000
                },
        }
        # Клик по кнопке "Марш"
        path_start_gather = resource_path(relative_path=self.locale.i10n('gather-marsh'))
        coord_start_gather = find_template_matches(path_start_gather)
        time.sleep(2)
        # Запускаем копание
        if coord_start_gather:
            logger.info(msg="GATHER: [STEP-9] CLICK TO YELLOW BUTTON - MARSH")
            self.clicker_manager.click(coord_start_gather[0][0], coord_start_gather[0][1])
            time.sleep(3)

            if self.gather_task['task'] in self.gather_stat:
                # Если есть - обновляем значения
                self.gather_stat[self.gather_task['task']]['count_gather'] += resourse_data[self.gather_task['task']][self.gather_task['get_lvl']]
                self.gather_stat[self.gather_task['task']]['count_task'] += 1
            else:
                # Если нет - создаем новую запись
                self.gather_stat[self.gather_task['task']] = {
                    'count_gather': resourse_data[self.gather_task['task']][self.gather_task['get_lvl']],
                    'count_task': 1
                }

            logger.info(msg="GATHER: [STEP-9] GATHER TASK COMLETED, TASK IS EMPTY")
            if self.gather_task['failed_count'] != 0:
                self.gather_task['failed_count'] = 0
                logger.info(msg=f"GATHER: [STEP-9] FAILED COUNT DROP TO 0")
            self.gather_task['task'] = None
            self.gather_task['lvl_down_task'] = False
            logger.info(msg=f"GATHER: [STEP-9] LVL DOWN TASK CHANGED TO - {self.gather_task['lvl_down_task']}")

            # Запускаем цикл на следующий отряд если нет другого задания
            if self.gather_task['additional_event_task']  == "gather" or self.gather_task['additional_event_task'] == "hunt" or self.gather_task['additional_event_task'] == "autorally":
                logger.info("GATHER: [STEP-9] Additional event is %s. Go to next gather task for troops", self.gather_task['additional_event_task'])
                # Запускаем цикл на следующий отряд
                return self.gather_step_1(window=window)
        else:
            logger.error(msg="GATHER: [STEP-9 COORD YELLOW BUTTON - MARSH NO DEFINED. NEED MORE TROOPS")
            # Закрываю окно выбора юнитов
            self.go_to_region()
            # Передаём управление другой программе
            # self.windows_index += 1
            logger.info(msg="GATHER: [STEP-9] GATHER TASK CAN NOT TO BE COMLETED, TASK IS EMPTY")
            if self.gather_task['failed_count'] != 0:
                self.gather_task['failed_count'] = 0
                logger.info(msg=f"GATHER: [STEP-9] FAILED COUNT DROP TO 0")
            self.gather_task['task'] = None
            self.gather_task['lvl_down_task'] = False
            logger.info(msg=f"GATHER: [STEP-9] LVL DOWN TASK CHANGED TO - {self.gather_task['lvl_down_task']}")

            # Если нет другого задания, то просто выходим в алгритм
            if self.gather_task['additional_event_task']  == "gather" or self.gather_task['additional_event_task'] == "hunt" or self.gather_task['additional_event_task'] == "autorally":
                logger.info("GATHER: [STEP-8] Additional event is %s. Go to next window", self.gather_task['additional_event_task'])
                return








### ================================= ZOMBI FARM ================================ ###
    @check_stop_func
    def zombi_step_0(self,window, task_data):
        self.zombi_task = task_data
        self.go_to_region()
        time.sleep(2)
        return self.zombi_step_1(window=window)
    @check_stop_func
    def zombi_step_1(self, window):
        if self.check_region_screen():
            time.sleep(2)
            if not self.zombi_task['hide_discount']:
                logger.info(msg="ZOMBI[STEP-1]: HIDE DISCOUNT TRIGGER - FALSE")
                self.hide_discont()
                self.zombi_task['hide_discount'] = True
                time.sleep(2)
            self.go_to_region()
            time.sleep(2)
            return self.zombi_step_2(window=window)

        else:
            logger.info(msg="ZOMBI[STEP-1]: REGION DON'T DETECTED - BACK IN STEP-1")
            self.go_to_region()
            time.sleep(3)
            return self.zombi_step_1(window=window)


    # Клик по поиску
    @check_stop_func
    def zombi_step_2(self, window):

        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=45, target_y=480)
        time.sleep(2)
        logger.info(msg="ZOMBI[STEP-2]: GO TO STEP-3 ")
        return self.zombi_step_3(window=window)

    # ДВИЖОК ВЫБОРА УРОВНЯ
    @check_stop_func
    def zombi_step_3(self, window):

        path_zombi = resource_path(relative_path="app\\windows\\shelter\\zombi\\img\\zombi.png")
        coord_zombi = find_template_matches(path_zombi)
        if coord_zombi and not self.task_manager.stop_event.is_set():
            logger.info(msg="ZOMBI[STEP-3]: FIND ZOMBI")
            self.clicker_manager.click(coord_zombi[0][0], coord_zombi[0][1])
            time.sleep(4)

        path_lvl_zombi = {i: resource_path(self.locale.i10n(f'zombi-lvl-{i}')) for i in range(5,41)}

        path_lvlup = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlup.png")
        path_lvldown = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvldown.png")
        path_lvlmax = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlmax.png")
        path_lvlmin = resource_path(relative_path="app\\windows\\shelter\\rally\\img\\lvlmin.png")
        current_lvl = 0
        for lvl, path in path_lvl_zombi.items():
            time.sleep(0.1)
            print(lvl, path)
            if self.task_manager.stop_event.is_set():
                break
            coord_lvl = find_template_matches(path, threshold=0.95)
            if coord_lvl:
                logger.info("ZOMBI[STEP-3]: GET CURRENT LVL: %s", lvl)
                current_lvl = lvl
                break
### ======
        # ТУТ Я НЕ СМОГ РАСПОЗНАТЬ ЦИФРЫ. СКОРЕЕ ВСЕГО СТОИТ УРОВЕНЬ 1-4.
        if current_lvl == 0:
            coord_lvlup = find_template_matches_color(path_lvlup)
            if coord_lvlup and not self.task_manager.stop_event.is_set():
                for i in range(4):
                    if self.task_manager.stop_event.is_set():
                        break
                    logger.info("ZOMBI[STEP-3]: LVL UP")
                    self.clicker_manager.click(coord_lvlup[0][0], coord_lvlup[0][1])
                    time.sleep(0.7)
            logger.info("ZOMBI[STEP-3]: FAILED GET CURRENT LVL. GO TO STEP - 1")

            return self.zombi_step_1(window=window)

        if current_lvl > self.zombi_task['max_zombi_lvl']-self.zombi_task['down_count']:
            # проверить не минимальный ли
            coord_lvlmin = find_template_matches_color(path_lvlmin, threshold=0.95)
            if coord_lvlmin and not self.task_manager.stop_event.is_set():
                logger.info("ZOMBI[STEP-3]: LVL MIN DETECTED. SKIP CHANGE")
            else:
                coord_lvldown = find_template_matches_color(path_lvldown)
                if coord_lvldown and not self.task_manager.stop_event.is_set():
                    for i in range(current_lvl-self.zombi_task['max_zombi_lvl']):
                        if self.task_manager.stop_event.is_set():
                            break
                        logger.info("ZOMBI[STEP-3]: LVL DOWN")
                        self.clicker_manager.click(coord_lvldown[0][0], coord_lvldown[0][1])
                        time.sleep(0.7)
                else:
                    logger.info("ZOMBI[STEP-3]: FAIL DETECTED LVL DOWN")

        if current_lvl < self.zombi_task['max_zombi_lvl']-self.zombi_task['down_count']:
            coord_lvlmax = find_template_matches_color(path_lvlmax, threshold=0.95)
            if coord_lvlmax:
                logger.info("ZOMBI[STEP-3]: LVL MAX DETECTED. SKIP CHANGE")
            else:
                coord_lvlup = find_template_matches_color(path_lvlup)
                if coord_lvlup and not self.task_manager.stop_event.is_set():
                    for i in range(abs(current_lvl-self.zombi_task['max_zombi_lvl'])):
                        if self.task_manager.stop_event.is_set():
                            break
                        logger.info("ZOMBI[STEP-3]: LVL UP")
                        self.clicker_manager.click(coord_lvlup[0][0], coord_lvlup[0][1])
                        time.sleep(0.7)
                else:
                    logger.info("ZOMBI[STEP-3]: FAIL DETECTED LVL UP")


        if current_lvl == self.zombi_task['max_zombi_lvl']-self.zombi_task['down_count']:
            logger.info("ZOMBI[STEP-3]: LVL IS GOOD")



        if self.zombi_task['down_triger']:
            logger.info("ZOMBI[STEP-3]: DOWN TRIGGER IS TRUE")
            coord_lvldown = find_template_simple(path_lvldown)
            if coord_lvldown and not self.task_manager.stop_event.is_set():
                for i in range(self.zombi_task['down_count']):
                    logger.info("ZOMBI[STEP-3]: LVL DOWN")
                    self.clicker_manager.click(coord_lvldown[0][0], coord_lvldown[0][1])
                    time.sleep(1)
        logger.info("ZOMBI[STEP-3]: GO TO STEP 4")
        return self.zombi_step_4(window=window)

    # Нажатие кнопки поиск в меню выбор
    @check_stop_func
    def zombi_step_4(self, window):
        path_poisk = resource_path(relative_path=self.locale.i10n('rally-poisk'))
        coord_poisk = find_template_matches_color(path_poisk)
        if coord_poisk and not self.task_manager.stop_event.is_set():
            logger.info("ZOMBI[STEP-4]: POISK DETECTED")
            self.clicker_manager.click(coord_poisk[0][0], coord_poisk[0][1])
            time.sleep(6)

        logger.info("ZOMBI[STEP-4]: GO TO STEP 5")
        return self.zombi_step_5(window=window)


    # Нажимаем на центр экрана(на зомби) чтобы появилась кнопка
    @check_stop_func
    def zombi_step_5(self, window):
        # Нажать на центр экрана чтоб выбрать zombie 640 390
        self.clicker_manager.proportion_click_in_window(window=window.window, target_x=640, target_y=390)
        time.sleep(3)
        logger.info("ZOMBI[STEP-5]: GO TO STEP 6")
        return self.zombi_step_6(window=window)

    # Ищем кнопку АТАКОВАТЬ
    @check_stop_func
    def zombi_step_6(self, window):
        # Найти кнопку аттаковать
        path_attack = resource_path(relative_path=self.locale.i10n('zombi-attack'))
        path_attack_list  = [
            path_attack
        ]
        coord_attack = []
        for path in path_attack_list:
            coord_attack = find_template_matches(path)
            if coord_attack and not self.task_manager.stop_event.is_set():
                logger.info("ZOMBI[STEP-6]: FIND ATTACK BUTTON")
                path_check_box = resource_path(relative_path="app\\windows\\shelter\\zombi\\img\\chk-box-fully.png")
                check_box_fully = find_template_matches(path_check_box, threshold=0.7)
                if check_box_fully:
                    # Тут я убедился что галочка стоит
                    logger.info(msg=f"ZOMBI[STEP-6]: CHECKBOX IS TRUE")
                    time.sleep(1)
                else:
                    logger.info(msg=f"ZOMBI[STEP-6]: CHECKBOX IS FALSE")
                    # Ищу пустой квадратик чтобы поставить галочку
                    path_check_box_empty = resource_path(relative_path="app\\windows\\shelter\\zombi\\img\\chk-box-empty.png")
                    coord_empty_checkbox = find_template_matches(path_check_box_empty, threshold=0.7)
                    if coord_empty_checkbox and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"ZOMBI[STEP-6]: FIND EMPTY CHECKBOX")
                        self.clicker_manager.click(coord_empty_checkbox[0][0], coord_empty_checkbox[0][1])
                        time.sleep(1)
                    else:
                        logger.info(msg=f"ZOMBI[STEP-6]: EMPTY CHECKBOX NOT FINDED")
                # Нажимаю атаковать
                logger.info(msg=f"ZOMBI[STEP-6]: PRESS ATTACK BTN")
                self.clicker_manager.click(coord_attack[0][0], coord_attack[0][1])
                time.sleep(4)
                logger.info("ZOMBI[STEP-6]: GO TO STEP 7")
                return self.zombi_step_7(window=window)
            else:
                logger.info("ZOMBI[STEP-6]: ATTACK BUTTON UNDEFIND")
                self.zombi_task['down_triger'] = True
                self.zombi_task['down_count'] += 1
                self.zombi_task['fail_count'] += 1
                logger.info("ZOMBI[STEP-6]: GO TO STEP 1")
                return self.zombi_step_1(window=window)

    @check_stop_func
    def zombi_step_7(self, window):
        path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
        path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
        # ВЫБИРАН РЕЖИМА МУЛЬТИОТРЯДОВ
        if self.zombi_task['multi_group']:
            path_mass_squad_create = resource_path(relative_path=self.locale.i10n('zombi-mass-create-squad'))
            coord_mass_squad_create = find_template_matches(path_mass_squad_create, threshold=0.7)
            # ИЩУ КНОПКУ МАСС ДЕПЛОЙ ЕСЛИ ОТРЯД НЕТ ИЛИ ВЫЗВАНЫ НЕ ВСЕ ОТРЯДЫ
            if coord_mass_squad_create and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"ZOMBI[STEP-7]: FIND MASS DEPLOY BTN")
                self.clicker_manager.click(coord_mass_squad_create[0][0], coord_mass_squad_create[0][1])
                time.sleep(2)
                path_chk_box_new_deploy = resource_path(relative_path="app\\windows\\shelter\\zombi\\img\\mass-chk-box-empty.png")
                coord_chk_box_new_deploy = find_template_matches(path_chk_box_new_deploy, threshold=0.7)
                # ИЩУ ЧЕКБОКС ЧТОБЫ ВЫЗВАТЬ ВСЕ ОТРЯДЫ
                if coord_chk_box_new_deploy and not self.task_manager.stop_event.is_set():
                    filter_coord = filter_coordinates(coords=coord_chk_box_new_deploy, threshold=10)
                    for x,y in filter_coord:
                        logger.info(msg=f"ZOMBI[STEP-7]: FIND EMPTY CHECKBOX")
                        self.clicker_manager.click(x=x, y=y)
                        time.sleep(1)
                path_mass_march_deploy = resource_path(relative_path=self.locale.i10n('zombi-mass-chk-box-march'))
                coord_mass_march_deploy = find_template_matches(path_mass_march_deploy, threshold=0.7)
                # ИЩУ ГАЛОЧКУ ВЫБРАТЬ ВСЕ ОТРЯДЫ. ОНА ЕСТЬ КОГДА В ПОЛЕ СТОЯТ МАКСИМУМ ОТРЯДОВ
                if coord_mass_march_deploy and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"ZOMBI[STEP-7]: FIND MARSH")
                    self.clicker_manager.click(coord_mass_march_deploy[0][0], coord_mass_march_deploy[0][1])
                    time.sleep(2)
                path_green_use = resource_path(relative_path=self.locale.i10n('radar-green-use'))
                path_green_half_empty = resource_path(relative_path="app\\img\\game_button\\green_half_empty.png")
                coord_green_use = find_template_matches(path_green_use)
                if coord_green_use and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"ZOMBI[STEP-7]: NO HAVE ENERGY")
                    green_count = 0
                    while not self.task_manager.stop_event.is_set():
                        if green_count == 15:
                            self.task_manager.stop_event.set()
                            return
                        coord_green_half = find_template_matches(path_green_half_empty)
                        if coord_green_half and not self.task_manager.stop_event.is_set():
                            coord_green_use_update = find_template_matches(path_green_use)
                            filter_coord = filter_coordinates(coord_green_use_update)
                            for x, y in filter_coord:
                                self.clicker_manager.click(x, y)
                                time.sleep(0.5)
                                green_count += 1
                        else:
                            self.clicker_manager.press_ecs()
                            time.sleep(1)
                            return self.zombi_step_1(window=window)
                else:
                    logger.info(msg=f"ZOMBI[STEP-7]: ENERGY IS GOOD")
                logger.info("ZOMBI[STEP-7]: GO TO STEP 8")
                return self.zombi_step_8(window=window)
            # КНОПКУ МАСС ДЕПЛОЙ НЕ НАШЕЛ. ЗНАЧИТ ВСЕ ОТРЯДЫ В ПОЛЕ
            else:
                logger.info(msg=f"ZOMBI[STEP-7]: MASS DEPLOY BTN UNDEFIND")
                path_mass_chk_box = resource_path(relative_path="app\\windows\\shelter\\zombi\\img\\select-mass-btn.png")
                coord_mass_chk_box = find_template_matches(path_mass_chk_box, threshold=0.7)
                # ИЩУ ГАЛОЧКУ ВЫБРАТЬ ВСЕ ОТРЯДЫ. ОНА ЕСТЬ КОГДА В ПОЛЕ СТОЯТ МАКСИМУМ ОТРЯДОВ
                if coord_mass_chk_box and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"ZOMBI[STEP-7]: FIND EMPTY CHECKBOX")
                    self.clicker_manager.click(coord_mass_chk_box[0][0], coord_mass_chk_box[0][1])
                    time.sleep(1)
                    # ИЩУ КНОПКУ МАРШ
                    path_mass_march = resource_path(relative_path=self.locale.i10n('zombi-mass-march'))
                    coord_mass_march = find_template_matches(path_mass_march, threshold=0.7)
                    if coord_mass_march and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"ZOMBI[STEP-7]: FIND MARSH")
                        self.clicker_manager.click(coord_mass_march[0][0], coord_mass_march[0][1])
                        time.sleep(2)
                    # ПРОВЕДРЯЖ ОКНО ЭНЕРГИИ

                    coord_green_use = find_template_matches(path_green_use)
                    if coord_green_use and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"ZOMBI[STEP-7]: NO HAVE ENERGY")
                        green_count = 0
                        while not self.task_manager.stop_event.is_set():
                            if green_count == 15:
                                self.task_manager.stop_event.set()
                                return
                            coord_green_half = find_template_matches(path_green_half_empty)
                            if coord_green_half and not self.task_manager.stop_event.is_set():
                                coord_green_use_update = find_template_matches(path_green_use)
                                filter_coord = filter_coordinates(coord_green_use_update)
                                for x, y in filter_coord:
                                    self.clicker_manager.click(x, y)
                                    time.sleep(0.5)
                                    green_count += 1
                            else:
                                self.clicker_manager.press_ecs()
                                time.sleep(1)
                                return self.zombi_step_1(window=window)
                    else:
                        logger.info(msg=f"ZOMBI[STEP-7]: ENERGY IS GOOD")
                    logger.info("ZOMBI[STEP-7]: GO TO STEP 8")
                    return self.zombi_step_8(window=window)

        # ТУТ ФАРМ ОДНИМ ОТРЯДОМ
        else:
            path_group_free_in_menu = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free_in_menu.png")
            coord_check_free_group = find_template_matches(path_group_free_in_menu)
            if coord_check_free_group and not self.task_manager.stop_event.is_set():
                self.clicker_manager.click(coord_check_free_group[0][0], coord_check_free_group[0][1])
                time.sleep(1)
                # Ищу кнопку Марш для отдыхающего отряда
                path_marsh_in_free_group = resource_path(relative_path=self.locale.i10n('radar-marsh-free-group'))
                coord_marsh_free_group = find_template_matches_color(path_marsh_in_free_group)
                if coord_marsh_free_group and not self.task_manager.stop_event.is_set():
                    self.clicker_manager.click(coord_marsh_free_group[0][0], coord_marsh_free_group[0][1])
                    time.sleep(2)
                    # Проверяю появилось ли окно то нет энергии
                    coord_green_use = find_template_matches(path_green_use)
                    if coord_green_use and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"ZOMBI[STEP-7]: NO HAVE ENERGY")
                        green_count = 0
                        while not self.task_manager.stop_event.is_set():
                            if green_count == 15:
                                self.task_manager.stop_event.set()
                                return
                            coord_green_half = find_template_matches(path_green_half_empty)
                            if coord_green_half and not self.task_manager.stop_event.is_set():
                                coord_green_use_update = find_template_matches(path_green_use)
                                filter_coord = filter_coordinates(coord_green_use_update)
                                for x, y in filter_coord:
                                    self.clicker_manager.click(x, y)
                                    time.sleep(0.5)
                                green_count += 1
                            else:
                                self.clicker_manager.press_ecs()
                                time.sleep(1)
                                return self.zombi_step_1(window=window)
                    else:
                        logger.info(msg=f"ZOMBI[STEP-7]: ENERGY IS GOOD")
                    logger.info("ZOMBI[STEP-7]: GO TO STEP 8")
                    return self.zombi_step_8(window=window)


            # Ищу кнопку Создать отряд
            else:
                path_create_group = resource_path(relative_path=self.locale.i10n('radar-create-group'))
                path_marsh = resource_path(relative_path=self.locale.i10n('radar-marsh'))
                coord_create_group = find_template_matches(path_create_group)
                if coord_create_group and not self.task_manager.stop_event.is_set():
                    logger.info(msg=f"ZOMBI[STEP-7]: CREATE GROUP BTN FIND")
                    self.clicker_manager.click(coord_create_group[0][0], coord_create_group[0][1])
                    time.sleep(3)
                    # Ищем кнопку Марш
                    coord_marsh = find_template_matches(path_marsh)
                    if coord_marsh and not self.task_manager.stop_event.is_set():
                        logger.info(msg=f"ZOMBI[STEP-7]: MARSH BTN FIND")
                        self.clicker_manager.click(coord_marsh[0][0], coord_marsh[0][1])
                        time.sleep(3)

                        # Проверяю появилось ли окно то нет энергии
                        coord_green_use = find_template_matches(path_green_use)
                        if coord_green_use and not self.task_manager.stop_event.is_set():
                            logger.info(msg=f"ZOMBI[STEP-7]: NO HAVE ENERGY")
                            green_count = 0
                            while not self.task_manager.stop_event.is_set():
                                if green_count == 15:
                                    self.task_manager.stop_event.set()
                                    return
                                coord_green_half = find_template_matches(path_green_half_empty)
                                if coord_green_half and not self.task_manager.stop_event.is_set():
                                    coord_green_use_update = find_template_matches(path_green_use)
                                    filter_coord = filter_coordinates(coord_green_use_update)
                                    for x, y in filter_coord:
                                        self.clicker_manager.click(x, y)
                                        time.sleep(0.5)
                                    green_count += 1
                                else:
                                    self.clicker_manager.press_ecs()
                                    time.sleep(1)
                                    return self.zombi_step_1(window=window)
                        else:
                            logger.info(msg=f"ZOMBI[STEP-7]: ENERGY IS GOOD")
                        logger.info("ZOMBI[STEP-7]: GO TO STEP 8")
                        return self.zombi_step_8(window=window)



    # ТУТ НАДО ПОДОЖДАТЬ ОКОНЧАНИЯ ФАРМА ЗОМБИ
    @check_stop_func
    def zombi_step_8(self, window):

        path_group_free = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free.png")
        path_group_free2 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free2.png")
        path_group_free3 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free3.png")
        path_group_free4 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free4.png")
        path_group_free5 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free5.png")
        path_group_free6 = resource_path(relative_path="app\\windows\\shelter\\radar\\img\\status_button\\group_free6.png")
        count_fail = 0
        path_free_group_list = [
            path_group_free,
            path_group_free2,
            path_group_free3,
            path_group_free4,
            path_group_free5,
            path_group_free6
        ]
        logger.info(msg=f"ZOMBI[STEP-8]: SLEEP 35 TO ROAD")
        time.sleep(35)

        while not self.task_manager.stop_event.is_set():
            # Тут я жду пока отряд убьет зомби или умрёт
            if count_fail > 180:
                self.zombi_task['fail_count'] += 1
                break
            end_fight = []
            for path in path_free_group_list:
                end_fight = find_template_simple(path, threshold=0.7)
                if end_fight:
                    break
            if end_fight and not self.task_manager.stop_event.is_set():
                logger.info(msg=f"ZOMBI[STEP-8]: END FIGHT")
                count_fail = 0
                break
            logger.info(msg=f"ZOMBI[STEP-8]: WAIT END FIGHT")
            time.sleep(1.5)
            count_fail += 2
        logger.info("ZOMBI[STEP-8]: GO TO STEP 9")
        return self.zombi_step_9(window=window)

    # ТУТ АЛГОРИТМ ОБРАБОТКИ ТРИГЕРОВ
    @check_stop_func
    def zombi_step_9(self, window):
            # "max_zombi_lvl" : self.zombi_lvl_var.get(),
            # "max_zombi_count": "",
            # "fail_count": 0,
            # "death_count": 0,
            # "stamina_trigger": False,
            # "down_triger": False,
            # "down_count": 0,
            # "hide_discount": False,
            # "start_zombi_timer": "",
            # "multi_group": self.var_multigrpup.get()
            # }

        self.zombi_task["zombi_count"] += 1
        logger.info("ZOMBI[STEP-9]: ZOMBIE COUNT INCREASE: [%s]", self.zombi_task["zombi_count"])
        self.zombi_task["zombi_repeat"] += 1
        logger.info("ZOMBI[STEP-9]: REPEAT INCREASE: [%s]", self.zombi_task["zombi_repeat"])


        if self.zombi_task["zombi_count"] > 0 and self.zombi_task["zombi_count"] % 10 == 0:
            logger.info("ZOMBI[STEP-9]: %10 RETRY SQUADS")
            self.back_all_group_home()
            logger.info("ZOMBI[STEP-9]: SLEEP 55 SEC TO HOME")
            time.sleep(55)

        if self.zombi_task["zombi_repeat"] > 0 and self.zombi_task["zombi_repeat"] % 2 == 0:
            logger.info("ZOMBI[STEP-9]: REPEAT %2. DOWN COUNT | DOWN TRIGGER")
            self.zombi_task["down_count"] += 1
            self.zombi_task["down_triger"] = True
        if self.zombi_task["zombi_repeat"] > 0 and self.zombi_task["zombi_repeat"] % 10 == 0:
            logger.info("ZOMBI[STEP-9]: REPEAT %10. DOWN COUNT | DOWN TRIGGER")
            self.zombi_task["down_count"] = 0
            self.zombi_task["down_triger"] = False


        if self.zombi_task["zombi_count"] == self.zombi_task["max_zombi_count"]:
            logger.info("ZOMBI[STEP-9]: TASK COMLETED")
            self.back_all_group_home()
            return
        else:
            logger.info("ZOMBI[STEP-9]: GO TO STEP 1")
            self.zombi_step_1(window=window)
