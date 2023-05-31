# CORS Bypass
1. The following CORS Bypass technique works when following conditions are met.
      1. If Cross origin is reflected back in Access-Control-Allow-Origin header and also if it has wildcard.
      2. If Cache-Control header is missing in the response. Even if it is present based on the values of the header we can check if the response is cached in browser.
      3. Also victim should have visited the endpoint/url prior to the attack such that the response is already cached in the browser.
 2. I have built a simple Web application in Python using Flask Web Framework.
      1. The App has two routes one is login once authenticated JWT is generated which is served back to the client such that it is stored in Local Storage and the second endpoint is protected where JWT token is verified before serving the response which contains the API key.
 3. Client side code is pretty self explanatory, username/password values are sent in the form of form data once authenticated access_token is stored in local storage and to access the protected resource access token is sent along with the request to fetch the API key.
 4. Once above conditions are met. it's time to Bypass CORS for Fun.
 5. Explanation of what payload is trying to accomplish?.
      1. we are adding a special header such that the request is served from cache instead of hitting the server.
      2. If we are adding additional headers such as Authorization preflight OPTIONS request is triggered by the browser to check if the server allows such headers. Feel free to tweak the payload as per your needs.
      3.  Finally when you run the script the response is fetched from the browser cache.

<img width="1266" alt="Burp" src="https://github.com/Srikanth9410/CORS/assets/36133052/8ac5a7c5-520f-4879-b960-9447d2d75ad1">
                  &nbsp;&nbsp;&nbspObserve that the Application has Access-Control-Allow-Origin set to wildcard and Cache-control Header is missing.<br><br><br>

<img width="997" alt="CORS" src="https://github.com/Srikanth9410/CORS/assets/36133052/b64315ea-88b8-4064-933b-35ee79add523">
                  &nbsp;&nbsp;&nbspObserve that once script is run the response is fetched from the disk space as shown.
