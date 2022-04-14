

/*
function htmlload() {
    alert("testing on load")
    if(sessionStorage.getItem('curColPath') === null)
    {
        sessionStorage.setItem('curColPath', '/collections')
    }

    
  }
*/

async function updateselect(n) {
    let selectobj = document.getElementById("data-select")
    if (n == 2) {
        selectobj = document.getElementById("feature-extract-select")
    }
    else if (n == 3) {
        selectobj = document.getElementById("model-select")
    }

    //loop through elements of select object and remove the selected object
    let selected = ""
    for (opt of selectobj.options) {
        if (opt.selected) {
            selected = opt.text
            break
        }

    }

    //call python for tufinterface remove:
    await eel.update_selection(selected, n)()

}


async function setpath(n) {
    //call python to use tk:
    let filepath = await eel.select_path()()

    if (filepath == "") {
        return;
    }

    //prompt for class name:
    let classname = window.prompt("Enter Class Name", "")

    if (classname == null) {
        return;
    }

    //call TufInterface.upload()
    let error = await eel.upload_path(classname, filepath, n)()
    if (error != null) {
        alert(error)
    }


}

async function runtest() {

    let dataname = ""
    for (opt of document.getElementById("data-select").options) {
        if (opt.selected) {
            dataname = opt.text
            break
        }
    }

    let fextractname = ""
    for (opt of document.getElementById("feature-extract-select").options) {
        if (opt.selected) {
            fextractname = opt.text
            break
        }
    }

    let modelname = ""
    for (opt of document.getElementById("model-select").options) {
        if (opt.selected) {
            modelname = opt.text
            break
        }
    }

    let cacheresults = document.getElementById("cache-check").checked;

    let error = await eel.run_test(dataname, fextractname, modelname, cacheresults)()
    if (error != null) {
        alert(error)
    }
}

async function removeselect(n) {
    let selectobj = document.getElementById("data-select")
    if (n == 2) {
        selectobj = document.getElementById("feature-extract-select")
    }
    else if (n == 3) {
        selectobj = document.getElementById("model-select")
    }

    //loop through elements of select object and remove the selected object
    let selected = ""
    for (opt of selectobj.options) {
        if (opt.selected) {
            selected = opt.text
            break
        }

    }

    //call python for tufinterface remove:
    let error = await eel.remove_path(selected, n)()
    if (error != null) {
        alert(error)
    }
}

function togglecheck() {
    eel.toggle_check()()
}

document.addEventListener("DOMContentLoaded", async function () {

    //use ti.get_entries from python for each type and populate select boxes:
    let data_elems = await eel.get_paths(1)()
    let fextractor_elems = await eel.get_paths(2)()
    let model_elems = await eel.get_paths(3)()
    let toggle = await eel.get_toggle()()



    for (let i = 0; i < data_elems.length; i++) {
        var option = document.createElement("option")
        option.text = data_elems[i]
        document.getElementById("data-select").add(option)
    }

    // add no option because fe is not required
    var option = document.createElement("option")
    option.text = "None"
    document.getElementById("feature-extract-select").add(option)

    for (let i = 0; i < fextractor_elems.length; i++) {
        var option = document.createElement("option")
        option.text = fextractor_elems[i]
        document.getElementById("feature-extract-select").add(option)
    }

    for (let i = 0; i < model_elems.length; i++) {
        var option = document.createElement("option")
        option.text = model_elems[i]
        document.getElementById("model-select").add(option)
    }

    if (toggle) {
        document.getElementById("cache-check").checked = true
    }

    //update selected items
    //get selections from python:
    let selected = await eel.get_selections()()
    
    let selectobj = document.getElementById("data-select")
    for (opt of selectobj.options) {
        if (opt.text == selected[0]) {
            opt.selected = true
            break
        }

    }
    selectobj = document.getElementById("feature-extract-select")
    for (opt of selectobj.options) {
        if (opt.text == selected[1]) {
            opt.selected = true
            break
        }

    }

    selectobj = document.getElementById("model-select")
    for (opt of selectobj.options) {
        if (opt.text == selected[2]) {
            opt.selected = true
            break
        }

    }

    //call python:

});
