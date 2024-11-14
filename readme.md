## Setup Instructions

1. **Install Python**

   Ensure that you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Prepare Libraries**

   Double-click `setup.bat` to install all the necessary Python libraries.

3. **Configure Files**

   There are two files you need to set up:

   ### 1. `glossary.txt`

   - Export glossary from NTR( json format ) and paste。

   ### 2. `settings.json`

   There are three variables to set:

   - **`authtoken`**

     - Open website main page, and copy it into the f12 console panel：

       ```javascript
       copy(JSON.parse(localStorage.getItem('authInfo')).profile.token);
       ```

     - After entered, the token would be copied to clipboard, back and paste。

   - **`link`**

     - Paste the favorite folder link。
     - For example:

       ```
       https://books.fishhawk.top/favorite/web/cbeabc97-7d74-410c-ae2e-fc72dff1a36f
       ```

   - **`delay`**

     - Request Delay，2-3 sec is good，do not make it too short，default value is 3 sec。

4. **Run the Program**

   Double-click `run.bat` to launch the program.