## Setup Instructions

1. **Install Python**

   Ensure that you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Prepare Libraries**

   Double-click `setup.bat` to install all the necessary Python libraries.

3. **Configure Files**

   There are two files you need to set up:

   ### 1. `glossary.txt`

   - 把需要的術語表綠站導出貼上就行。

   ### 2. `settings.json`

   There are three variables to set:

   - **`authtoken`**

     - 打開綠站主頁，輸入這串指令：

       ```javascript
       copy(JSON.parse(localStorage.getItem('authInfo')).profile.token);
       ```

     - 打完之後會自動複製 token，到這貼上就行。

   - **`link`**

     - 貼上你要批量加入術語表的收藏夾鏈接。
     - 例如（for example）:

       ```
       https://books.fishhawk.top/favorite/web/cbeadb97-7d74-410c-ae2c-fca1df11a36f
       ```

   - **`delay`**

     - 請求頻率，2-3 秒差不多，最好別太低，預設是 3 秒。

4. **Run the Program**

   Double-click `run.bat` to launch the program.