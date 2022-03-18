import webview
import os
from PIL import Image

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
        height: 400px;
    }

    #innerCard{
        background-color: #282a2e;
        margin-top: 25px; 
        height: 305px;
        margin-left: 22px;
        margin-right: 22px;
    }

    #mainbtn{
        margin-top: 10px;
    }
</style>
</head>
<body>

<center><h1 id="tsk" class="text-warning">Image Operation</h1></center>

<center>
    <div id="innerCard">
        <div>
            <br><br>
            <div class="input-group mb-3 px-2">
                <span class="input-group-text" id="basic-addon1">Folder Path</span>
                <input placeholder="e,g. /home/usr/abc/" id="dir" type="text" class="form-control">
            </div>
            <div class="input-group mb-3 px-2">
                <span class="input-group-text" id="basic-addon1">Rename With</span>
                <input placeholder="Type without extension..." id="ren" type="text" class="form-control">
            </div>
            <div class="row px-2">
                <div class="col-md" style="width: 310px; display: none;">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">Compress Size</span>
                        <input placeholder="e,g. 20KB" id="comSize" type="text" class="form-control">
                    </div>
                </div>
                <div class="col-md">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">Dimension</span>
                        <input placeholder="e,g. 300x300" id="dim" type="text" class="form-control">
                    </div>
                </div>
            </div>
            <button onclick="run()" type="button" class="btn btn-outline-warning btn-lg" id="hibtn">
                <span id="r">Run</span>
                <div class="spinner-border" role="status" id="w" style="display: none;">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </button>
        </div
    </div>
</center>

<script>
    function endsWith(str, suffix) {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    }

    function run() {
        var ren = document.getElementById("ren").value;
        var comSize = document.getElementById("comSize").value;
        var dim = document.getElementById("dim").value;
        var dir = document.getElementById("dir").value;

        if(dir.trim() != ""){ 
            if(endsWith(dir, "/")){
                document.getElementById("w").style.display = 'block';
                document.getElementById("r").style.display = 'none';
                document.getElementById("hibtn").disabled = true;
                pywebview.api.run(dir, ren, comSize, dim).then(showResponse);
            }else{
                alert("Folder must be end with /");
            }
        }else{
            alert("Folder(location) field can't be empty");
        }
        
    }

    function showResponse(response) {
        alert(response);
        document.getElementById("w").style.display = 'none';
        document.getElementById("r").style.display = 'block';
        document.getElementById("hibtn").disabled = false; 
    }

</script>
</body>
</html>
"""


class Api:
    def __init__(self):
        self.required_op_dict = {}

    def filterReqOp(self, ren, comSize, dim):
        comSize = comSize.upper()
        dim = dim.lower()
        required_op = [ren, comSize.upper(), dim]
        if ren == "":
            required_op.remove(ren)
        else:
            self.required_op_dict['renamewith'] = ren
        if comSize == "":
            required_op.remove(comSize)
        else:
            self.required_op_dict['compressSize'] = comSize
        if dim == "":
            required_op.remove(dim)
        else:
            self.required_op_dict['dimension'] = dim

    def checkValid(self):
        dimStatus = True
        comSize_status = True
        return_msg = "Please go with any operation !!!"

        # CHECK FOR COMPRESS SIZE
        try:
            comSize = self.required_op_dict['compressSize']
        except: 
            comSize_status = False
        if comSize_status:
            if "K" in comSize:
                splitData = comSize.split("K", 1)
                if len(splitData) == 2:
                    if splitData[1] == "B" and splitData[0].isnumeric():
                        return_msg = "Valid"
                    else:
                        return "Compress Size Not Valid ..."
                else:
                    return "Compress Size Not Valid ..."
            elif "M" in comSize:
                splitData = comSize.split("M", 1)
                if len(splitData) == 2:
                    if splitData[1] == "B" and splitData[0].isnumeric():
                        return_msg = "Valid"
                    else:
                        return "Compress Size Not Valid ..."
                else:
                    return "Compress Size Not Valid ..."
            else:
                return "Compress Size Not Valid ..."
        

        # CHECK FOR DIMENSION
        try:
            dim = self.required_op_dict['dimension']
        except:
            dimStatus = False
        if dimStatus:
            if 'x' in dim:
                dimSplitData = dim.split('x', 1)
                if len(dimSplitData) == 2:
                    if dimSplitData[0].isnumeric() and dimSplitData[1].isnumeric():
                        return_msg = "Valid"
                    else:
                        return "Invalid Dimension !!!"
                else:
                    return "Invalid Dimension !!!"
            else:
                return "Invalid Dimension !!!"

        # CHECK FOR Rename
        try:
            renstatus = self.required_op_dict['renamewith']
        except:
            renstatus = False

        if renstatus:
            if len(self.required_op_dict['renamewith'])>0:
                return_msg = "Valid"
        return return_msg

    def renameAllImages(self, dir, ren):
        allFiles = os.listdir(dir)
        allImages = []
        possibleExt = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff','.psd']
        for i in allFiles:
            fileName, fileExtension = os.path.splitext(i)
            if fileExtension in possibleExt:
                allImages.append(i)

        # NOW YOU HAVE THE ALL IMAGES
        if len(allImages)<=0:
            return "There is no image in this location...."
        else:
            for index, i in enumerate(allImages):
                _, fileExtension = os.path.splitext(i)
                os.rename(dir+str(i), dir+ren+str(index+1)+fileExtension)
            return "done"

    def dimensionImage(self, dir, dim):
        try:
            os.mkdir(dir+"TaskStore/")
        except:
            pass
        allFiles = os.listdir(dir)
        allImages = []
        possibleExt = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff','.psd']
        for i in allFiles:
            fileName, fileExtension = os.path.splitext(i)
            if fileExtension in possibleExt:
                allImages.append(i)
        w, h = dim.split("x")
        for i in allImages:
            img = Image.open(dir+i)
            img = img.resize((int(w),int(h)), Image.ANTIALIAS)
            img.save(dir+f"TaskStore/{i}")
        return "done"

    def run(self, dir, ren, comSize, dim):
        self.filterReqOp(ren, comSize, dim)
        ret_data = self.checkValid()

        if ret_data == "Valid":
            # TRY TO RENAME THE FILE
            if ren != "":
                res = self.renameAllImages(dir, ren)
                if res != "done":
                    return res
            if dim != "":
                res = self.dimensionImage(dir, dim)
                if res != "done":
                    return res
            return "Successfully Executed !!!"
            
        else:  
            return ret_data
            


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Task Store', html=html, js_api=api,  width=700, height=450)
    webview.start()
