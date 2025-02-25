import time
from core.pcr_config import debug
from core.constant import SHOP_BTN
from automator_mixins._tools import ToolsMixin
from DataCenter import LoadPCRData
from core.cv import UIMatcher
import cv2


def get_frag_img_path(charname):
    data = LoadPCRData()
    a = str(data.get_id(name=charname))
    b = str(f"3{a[:4]}")
    return f"img/shop/frags/{b}.bmp"


class ShopMixin(ToolsMixin):

    def show_coin(self, screen=None):
        self.check_ocr_running()
        if screen is None:
            screen = self.getscreen()
        at = (789, 16, 918, 32)
        out = self.ocr_int(*at, screen_shot=screen)
        if debug:
            self.log.write_log('debug', f"持有代币：{out}")
        return out

    def buy_press(self):
        self.click(791, 435)
        # 点击购买
        time.sleep(1)
        self.click(591, 468)
        # 购买确认
        time.sleep(1.5)
        self.click(477, 473)
        # 买完提示
        time.sleep(2)

    def tick_frag(self, fraglist=None):
        if fraglist is None:
            self.log.write_log('warning',"无该类型碎片")
            return
        drag_count = 0
        buy_count = 0
        while True:

            if drag_count > 3:
                if not self.is_exists(SHOP_BTN["jiechusuoyou"]):
                    return
                if buy_count > 0:
                    self.buy_press()
                    return
                return

            for frag_ in fraglist[:]:
                imgpath_ = get_frag_img_path(charname=frag_)
                a = self.click_frag(imgpath=imgpath_)
                if a == 0:
                    buy_count += 1
                    fraglist.remove(frag_)
                    self.log.write_log('info',str(fraglist))
                    if len(fraglist) != 0:
                        continue
                    if self.is_exists(SHOP_BTN["jiechusuoyou"]):
                        self.buy_press()
                    return
                else:
                    self.dragdown()
                    time.sleep(3)
                    drag_count = drag_count + 1
                    continue

    def click_frag(self, imgpath):
        # 寻找单个碎片，确认碎片图片中心点
        screen = self.getscreen()
        # at = (241, 105, 925, 392)
        at = (278, 109, 890, 269)
        r_list = UIMatcher.img_where(screen, imgpath, threshold=0.8, at=at,
                                     method=cv2.TM_CCOEFF_NORMED, is_black=False, black_threshold=1500)
        # r_list = self.img_where_all(img=imgpath, at=(241, 105, 925, 392))
        # 根据偏移，点击勾选碎片
        if r_list is not False and len(r_list) == 2:
            x_arg = int(r_list[0]) + 57
            y_arg = int(r_list[1]) - 16
            self.click(x_arg, y_arg)
            return 0
        else:
            return 2

    def dragdown(self):
        obj = self.d.touch.down(584, 377)
        time.sleep(0.1)
        obj.move(584, 110)
        time.sleep(0.8)
        obj.up(584, 110)

    def buy_all_frag(self, dxc_fraglist=None, jjc_fraglist=None, pjjc_fraglist=None, clan_fraglist=None):
        self.lock_home()
        # 进入商店
        self.click(617, 435)
        time.sleep(2)
        # 地下城碎片
        self.click(359, 65)
        self.click_btn(SHOP_BTN["dxc_btn"], until_appear=SHOP_BTN["dxc_coin"])
        time.sleep(1)
        coin = self.show_coin()
        a = len(dxc_fraglist)
        if coin >= 800 * a:
            self.tick_frag(fraglist=dxc_fraglist)
        self.log.write_log('info',"地下城购买完毕")
        time.sleep(2)
        # JJC碎片
        self.click(454, 65)
        self.click_btn(SHOP_BTN["jjc_btn"], until_appear=SHOP_BTN["jjc_coin"])
        time.sleep(2)
        coin = self.show_coin()
        a = len(dxc_fraglist)
        if coin >= 800 * a:
            self.tick_frag(fraglist=jjc_fraglist)
        self.log.write_log('info',"JJC购买完毕")
        time.sleep(2)
        # PJJC碎片
        self.click(543, 65)
        self.click_btn(SHOP_BTN["pjjc_btn"], until_appear=SHOP_BTN["pjjc_coin"])
        time.sleep(2)
        coin = self.show_coin()
        a = len(dxc_fraglist)
        if coin >= 800 * a:
            self.tick_frag(fraglist=pjjc_fraglist)
        self.log.write_log('info',"PJJC购买完毕")
        time.sleep(2)
        # 行会碎片
        self.click(640, 65)
        self.click_btn(SHOP_BTN["clan_btn"], until_appear=SHOP_BTN["clan_coin"])
        time.sleep(2)
        coin = self.show_coin()
        a = len(dxc_fraglist)
        if coin >= 800 * a:
            self.tick_frag(fraglist=clan_fraglist)
        self.log.write_log('info',"行会购买完毕")
        self.lock_home()
