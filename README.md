# TCGS_Asking

## 功能簡介
	可透過使用者輸入的關鍵字搜尋臉書粉專「發問中女中」當中的貼文

## BOT位置
* 臉書專業名稱：Test_
* id：1914622091992882

## 使用方式
* 在Facebook For Developers 更新 Webhooks 回呼網址
* 從Facebook For Developers 的圖形API工具得到存取權杖，更新utils.py的SPIDER_TOKEN

## 功能細節
* 輸入任意字串開始使用
* 當看見「請問需要什麼服務呢」有四種回應選擇，輸入其他內容會直接忽略
	* 「搜尋」：依照引導輸入想搜尋的任意字串，以及最多顯示貼文數目。BOT會回應找到的貼文內容。
	* 「關閉」：關閉BOT服務，可隨時透過輸入「restart」再次開啟。
	* 「help」：BOT將回應使用方式。
	* 「iloveyou」：BOT彩蛋。

## State Diagram
	<待補>
	
## 作業要求確認
* Basic Requirement:皆符合
* Bonus:
	* More messenger functionalities:傳送按鈕與圖片
	* Dynamic data:讀取臉書粉絲專業貼文
	* others:爬取臉書Graph API response