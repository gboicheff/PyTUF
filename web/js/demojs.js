


function htmlload() {
    alert("testing on load")
    
  }


document.addEventListener("DOMContentLoaded", async function() {
    

    folderelems = await eel.get_folder()()

    
    folderelems.forEach(elem => {
        alert(elem)
        var option = document.createElement("option")
        option.text = elem
        document.getElementById("data-select").add(option)
    });



    //call python:
    
});
