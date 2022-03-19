

/*
function htmlload() {
    alert("testing on load")
    if(sessionStorage.getItem('curColPath') === null)
    {
        sessionStorage.setItem('curColPath', '/collections')
    }

    
  }
*/
async function setpath(n) {
    //call python to use tk:
    newcolfold = await eel.select_path()()

    if(n == 1)
    {
        sessionStorage.setItem('curColPath', newcolfold)
    }
    else if(n == 2)
    {
        sessionStorage.setItem('curExtractPath', newcolfold)
    }
    else if(n == 3)
    {
        sessionStorage.setItem('curScoringPath', newcolfold)
    }

}


document.addEventListener("DOMContentLoaded", async function() {
    

    if(sessionStorage.getItem('curColPath') === null)
    {
        sessionStorage.setItem('curColPath', '/collections')
    }
    if(sessionStorage.getItem('curExtractPath') === null)
    {
        sessionStorage.setItem('curExtractPath', '/collections')
    }
    if(sessionStorage.getItem('curScoringPath') === null)
    {
        sessionStorage.setItem('curScoringPath', '/collections')
    }

    folderelems = await eel.get_folder(sessionStorage.getItem('curColPath'))()
    folderelems.forEach(elem => {
        var option = document.createElement("option")
        option.text = elem
        document.getElementById("data-select").add(option)
    });


    folderelems = await eel.get_folder(sessionStorage.getItem('curExtractPath'))()
    folderelems.forEach(elem => {
        var option = document.createElement("option")
        option.text = elem
        document.getElementById("feature-extract-select").add(option)
    });


    folderelems = await eel.get_folder(sessionStorage.getItem('curScoringPath'))()
    folderelems.forEach(elem => {
        var option = document.createElement("option")
        option.text = elem
        document.getElementById("scoring-exclusion-select").add(option)
    });



    //call python:
    
});
