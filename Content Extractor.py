from goose3 import Goose
import webview
import os
import shutil

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>


<style>
    #tsk{
        color: #b5b8bd;
        margin-top: 10px;
    }

    body{
        background-color: #111317;
        height: 250px;
    }

    #innerCard{
        background-color: #282a2e;
        margin-top: 15px; 
        height: 220px;
        margin-left: 22px;
        margin-right: 22px;
    }

    #mainbtn{
        margin-top: 10px;
    }
</style>
</head>
<body>

<center><h1 id="tsk">Content Extractor</h1></center>

<center>
    <div id="innerCard">
        <div>
            <br>
            <div class="form-floating mx-3 mb-3">
                <input type="text" class="form-control" id="url" placeholder="Enter the url">
                <label for="url">URL</label>
            </div>
            <button onclick="run()" id="mainbtn" type="button" class="btn btn-secondary btn-lg">
                <span id="r">Run</span>
                <div class="spinner-border" role="status" id="w" style="display: none">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </button>
        </div
    </div>
</center>

<script>
    function run() {
        var url = document.getElementById("url").value;
        if(url.trim() != ""){
            document.getElementById("w").style.display = 'block';
            document.getElementById("r").style.display = 'none';
            document.getElementById("mainbtn").disabled = true; 
            pywebview.api.getFile(url).then(showResponse);
        }else{
            alert("Please fill all fields...");
        }
        
    }

    function showResponse(response) {
        alert("Done!!!, check your desktop for data...");
        document.getElementById("w").style.display = 'none';
        document.getElementById("r").style.display = 'block';
        document.getElementById("mainbtn").disabled = false; 
    }
</script>
</body>
</html>
"""

class Api:
    def getFile(self, url):
        g = Goose()
        article = g.extract(url=url)
        home = os.path.expanduser('~')
        location = os.path.join(home, 'Desktop')
        with open(f"{location}/ScrappingData.txt", "a") as f:
            f.writelines(f"###########################################{article.title}###########################################\n\n")
            f.write(article.cleaned_text)
        return "done"
            


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Task Store', html=html, js_api=api,  width=700, height=300)
    webview.start()