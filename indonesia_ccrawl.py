import sys
sys.path.append("c:\\Castko\\code")

from utils import CrawlUtil, JSONUtil #DBUtil, JSONUtil
from logger import Logger

from datetime import datetime
import time


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
#### 수정해야할 것 ####

# 1. main 함수에서 code_desc 기능 넣기
# 2. except 구문에서 browser.quit() 넣기 for 자원 낭비하지 x 
# 3. time.sleep() 줄이기 -> 좀만 더 줄이자
# 4. 서버에서 테스트 필요
# 5. fta_dict에 없는 fta명은 pass하기
# 6. 98번대 제거
# 7. 현재 정보 soup으로 가져온 뒤에 click_dt 확인하기


# 7304를 검색하면 98053020이 출력됩니당! 97번까지 있다고 알고 있는데 버리나요? -> 내부 논의 필요하다고 함.
# 98...은 tarif preferensi가 없어요~! 

class indonesia():

    fta_dict={
        # ATIGA
        "atiga":["brn_atiga", "mmr_atiga", "khm_atiga", "mys_atiga", 
              "lao_atiga", "phl_atiga", "sgp_atiga", "tha_atiga", "vnm_atiga"], 
        # RCEP 
        "rcep-japan":["jpn_rcep"],"rcep-china":["chn_rcep"],"rcep-korea":["kor_rcep"],
        "rcep-australia":["aus_rcep"],"rcep-new":["nzl_rcep"],
        "rcep-asean":["brn_rcep_asean", "khm_rcep_asean", "mys_rcep_asean", "lao_rcep_asean", "phl_rcep_asean", 
                      "sgp_rcep_asean", "tha_rcep_asean", "vnm_rcep_asean", "aus_rcep_asean", "nzl_rcep_asean", 
                      "kor_rcep_asean", "chn_rcep_asean", "jpn_rcep_asean"],
        # AUS 
        "aanzfta":["aus_aanzfta", "nzl_aanzfta"],"iacepa":["aus_iacepa"],
        # HKG 
        "ahkfta":["hkg_ahkfta"],
        # CHN 
        "acfta":["chn_acfta"],
        # IND 
        "aifta":["ind_aifta"],
        # JPN 
        "ajcep":["jpn_ajcep"],
        "ijepa":["jpn_ijepa"],
        # KOR 
        "akfta":["kor_akfta"],
        "ikcepa":["kor_ikcepa"],
        # CHL 
        "iccepa":["chl_iccepa"],
        # EFTA 
        "iecepa":["che_iecepa","lie_iecepa", "nor_iecepa", "isl_iecepa"],
        # PAK 
        "ippta":["pak_ippta"],
        # ARE 
        "iuae-cepa":["are_iuae_cepa"],
        # D8 
        "preferential":["bgd_d8","egy_d8","mys_d8","irn_d8","nga_d8","pak_d8","tur_d8"],
        # TPS-OIC -> None
        # Others 
        "impta":["moz_impta"],"ipapta":["pse_ipapta"],"usdfs":["jpn_usdfs_ijcepa"] # USDFS - IJCEPA (User Specific Duty Free Scheme - Indonesia Japan CEPA)
    }

    url = "https://www.insw.go.id/intr"
    front_list=[str(i).zfill(2) for i in range(1,98)]

    @staticmethod
    def get_code_desc_list(logger, browser): # soup말고 driver을 인자로 가져옴
        """
        - get HS code and description
        :param logger:
        :param browser:
        :return: list [{"code":str, "description":str},...]
        """

        try:
            # 0101검색
            browser.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/input").send_keys("0101")
            browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div/span/img").click()
            time.sleep(1)
            code_list=[]
            des_list=[]

            for element in browser.find_elements(By.TAG_NAME, "tr"):
                elem=element.text.split("\n")
                if len(elem)==1: # 버릴 것
                    continue
                try:
                    int(elem[0][0]) # 첫번째 원소가 int형 변환 가능
                    code_list.append(elem[0])
                    des_list.append(elem[2].replace('- ','')) # description에서 '-'버리기
                except: 
                    continue
            
            # 자리이동
            for f in indonesia.front_list: 
                if f=='01':
                    rear=1 # 0102 검색
                else:
                    rear=0 # 0201 검색
                
                while True: # 뒷자리 이동 -> 언제까지인지 모름
                    rear+=1

                    # 기존에 검색한 값 초기화
                    browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/input").clear()
                    time.sleep(1)

                    # 검색 코드 갱신, 검색
                    search=str(f)+str(rear).zfill(2)

                    browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/input").send_keys(search)
                    time.sleep(0.5)
                    browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div").click()
                    time.sleep(1)

                    if len(browser.find_elements(By.TAG_NAME, "tr"))==0: # 코드 없으면 앞 자리수 이동
                        break

                    # 정보 저장
                    for element in browser.find_elements(By.TAG_NAME, "tr"):
                        elem=element.text.split("\n")

                        if len(elem)==1: # 버릴 것
                            continue

                        try:
                            int(elem[0][0]) # 첫번째 원소가 int형 변환 가능
                            code_list.append(elem[0])
                            des_list.append(elem[2].replace('- ','')) # description에서 '-'버리기
                        except: 
                            continue
                            
                    # 다음 페이지 존재 여부 확인
                    # 1. 스크롤 맨 끝까지 내리기
                    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                    time.sleep(0.5)
                    
                    page=2
                    while True:
                        try:
                            # 다음 페이지 이동
                            browser.find_element(By.XPATH,"//*[contains(@aria-label,'Page "+str(page)+"')]").click()
                            time.sleep(0.5)

                            # 정보 저장
                            for element in browser.find_elements(By.TAG_NAME, "tr"):
                                elem=element.text.split("\n")
                                if len(elem)==1: # 버릴 것
                                    continue
                                try:
                                    int(elem[0][0]) # 첫번째 원소가 int형 변환 가능
                                    code_list.append(elem[0])
                                    des_list.append(elem[2].replace('- ','')) # description에서 '-'버리기
                                except: 
                                    continue
                            page+=1
                        except:
                            break
            
            result_dict_list = []
            for c,d in zip(code_list, des_list):
                result_dict=[]
                result_dict['code']=c
                result_dict['description']=d
                result_dict_list.append(result_dict)
            return result_dict_list
        
        except Exception as e:
            logger.error("[Fail][indonesia_all]get_code_desc_list")
            logger.error("Error : ", e)

    @staticmethod
    def click_dt(logger,browser,i):
        """
        - Click the detail button
        :param logger:
        :param browser:
        :param i: -> button index
        :return: browser's height
        """
        try:
            tabindx=browser.find_element(By.XPATH,"//*[contains(@tabindex,'"+str(i)+"')]")
            try:
                tabindx.find_element(By.XPATH,'button').click()
                time.sleep(1.5)
            except:
                pass
            height2=browser.execute_script("return document.body.scrollHeight")
            return height2
        except Exception as e:
            logger.error("[Fail][indonesia_all]click_dt")
            logger.error("Error : ", e)
    
    @staticmethod
    def click_tarif(logger,browser):
        """
        - Click the tarif preferensi button
        :param logger:
        :param browser:
        """
        try:
            for i in range(20):
                try:
                    browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr["+str(i)+"]/td/div/div[4]/div[1]").click()
                    time.sleep(1)
                except:
                    pass
        except Exception as e:
            logger.error("[Fail][indonesia_all]click_tarif")
            logger.error("Error : ", e)

    @staticmethod
    def current_soup(logger,browser,count):
        """
        - get current browser information to soup
        :param logger:
        :param browser:
        :return: soup
        """
        try:
            html=browser.page_source
            soup=BeautifulSoup(html,'html.parser')
            # detail 활성화 되었는지 확인
            if len(soup.find_all(class_='collapse-container'))==0: 
                # 현재 정보가 갱신될 때 까지 click_dt, click_tarif 실행

                height = browser.execute_script("return document.body.scrollHeight") # 현재 높이
                count-=1 # 현재 눌린 detail 재클릭해서 없애고 현재 detail 부터 클릭
                height2=indonesia.click_dt(logger,browser,4*count) # 현재 눌린 detail 없애기
                time.sleep(1)
                
                while True:
                    height2=indonesia.click_dt(logger,browser,4*count) # 현재 눌린 detail 다시 누르기
                    time.sleep(1)
                    count+=1
                    if height<height2:
                        break
                # 다시 tarif preferensi 클릭
                indonesia.click_tarif(logger,browser)

                html=browser.page_source
                soup=BeautifulSoup(html,'html.parser')
            return soup
        except Exception as e:
            logger.error("[Fail][indonesia_all]current_soup")
            logger.error("Error : ", e)

    @staticmethod
    def get_hscode_list(logger,browser):
        """
        - get hs code list in current browser
        :param logger:
        :param browser:
        :return: ['01012100', ...]
        """
        try:
            # 현재 페이지의 hs-code 정보 가져오기
            code_list=[]
            for hs in range(4,45,4):
                try:
                    code=browser.find_element(By.XPATH,"//*[contains(@tabindex,'"+str(hs-3)+"')]").text#click() #none반환
                    if len(code)==8:
                        code_list.append(code)
                except:
                    pass
            time.sleep(1)
            return code_list

        except Exception as e:
            logger.error("[Fail][indonesia_all]get_hscode_list")
            logger.error("Error : ", e)

    @staticmethod
    def get_tarif_list(logger,soup, code_list):
        try:
            page_dict_list = []
            for i in range(len(code_list)):
                code_dict=dict()
                code_dict['hs_code']=code_list[i]
                code_dict['strd_yr']='2024' ######### 변경해야함 #######
                code_dict['created_dt']='20240130'
                code_dict['update_dt']='20240130'
                
                tables=soup.find_all(class_='komoditas-detail-konten')[i] 
                inform_tarif=tables.find_all(class_='collapse-container')[1]
                bm=inform_tarif.find_all('p')[5].text
                code_dict['comm_mfn']=str(bm)
                
                tarif_prefer=tables.find_all(class_='collapse-container')[3]
                ftas=tarif_prefer.find_all('li') # fta별 정보
                
                for i in ftas:
                    if i['class'][0]=='collapse-text': # fta이름
                        key=i.text.split(' ')[0].lower()
                    else: # 세율        
                        for f in indonesia.fta_dict[key]:
                            if f in code_dict: # 이미 값이 있으면 pass (과거 정보)
                                continue
                            else:
                                code_dict[f]=i.text.split(' ')[-1]
                                # values['strd_yr']=i.text.split(' ')[1] ##############여기 변경해야함 #############
            
                page_dict_list.append(code_dict)
            return page_dict_list
        
        except Exception as e:
            logger.error("[Fail][indonesia_all]get_tarif_list")
            logger.error("Error : ", e)


####### code_desc 추가하는 코드 넣어야 함!!! ##########
def indonesia_main(logger):
    browser=CrawlUtil.get_browser(logger)
    CrawlUtil.start_browser(logger, browser, indonesia.url) # (logger,browser,url):
    ### 0101 검색 ###
    browser.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/input").send_keys("0101")
    time.sleep(0.5)
    browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div/span/img").click()
    time.sleep(1)

    code_list=indonesia.get_hscode_list(logger,browser)

    # detail, tarif 누르기 
    height = browser.execute_script("return document.body.scrollHeight")
    count=1
    while True:
        height2=indonesia.click_dt(logger,browser,4*count)
        time.sleep(0.5)
        count+=1
        if height!=height2:
            break
    indonesia.click_tarif(logger,browser)

    # 현재 정보 soup로 가져오기
    soup=indonesia.current_soup(logger,browser,count) 
    code_dict_list = indonesia.get_tarif_list(logger,soup, code_list)

    ### 자리 수 이동 ###
    for front in indonesia.front_list: # 앞자리 이동
        if front=='01':
            rear=1 # 0102 검색
        else:
            rear=0 # 0201 검색
        
        while True: # 뒷자리 이동 -> 언제까지인지 모름
            rear+=1
            browser.execute_script("window.scrollTo(0,0);")
            
            # 기존에 검색한 값 초기화
            browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/input").clear()
            time.sleep(0.5)
            # 검색 코드 갱신, 검색
            search=str(front)+str(rear).zfill(2)
            browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/input").send_keys(search)
            time.sleep(0.5)
            browser.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div").click()
            time.sleep(1)

            # 코드 없으면 앞 자리수 이동
            if len(browser.find_elements(By.TAG_NAME, "tr"))==0: 
                break
                
            # 현재 페이지의 hs-code 정보 가져오기
            code_list=indonesia.get_hscode_list(logger,browser)
            # detail 누르기 
            height = browser.execute_script("return document.body.scrollHeight")
            count=1
            while True:
                height2=indonesia.click_dt(logger,browser,4*count)
                time.sleep(1)
                count+=1
                if height!=height2:
                    break
            indonesia.click_tarif(logger,browser)

            # 현재 정보 soup로 가져오기
            soup=indonesia.current_soup(logger,browser,count)
            code_dict_list.extend(indonesia.get_tarif_list(logger,soup, code_list))
    
    CrawlUtil.quit_browser(logger,browser)
    JSONUtil.write_json(logger, code_dict_list, "./output/japan_tariff_list.json")






logger = Logger.get_logger('indonesia')
# Logger.set_logger('indonesia')
indonesia_main(logger)    

            
# if __name__ == '__main__':
#     start = time.time()
#     # set logging
#     logger = Logger.get_logger()
#     Logger.set_logger()

#     # main call
#     indonesia_main(logger)

#     end = time.time()

#     elapsed = end - start
#     print("time", elapsed/60, "min")