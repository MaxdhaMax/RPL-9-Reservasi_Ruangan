function SetActivateContent(id) {
    document.querySelectorAll(".main-content .page-item").forEach((opsi) => {
        if(opsi.id.charAt(opsi.id.length - 1) === id){
            opsi.classList.add("active")
        }
        else{
            opsi.classList.remove("active")
        }        
    })
    document.querySelectorAll(".main-content .content-page").forEach((content) => {
        if(content.id.charAt(content.id.length - 1) === id){  
            content.style.display = "block"
        }
        else{
            content.style.display = "none"
        }
    })
}

SetActivateContent("1")

document.querySelectorAll(".main-content .page-item").forEach((opsi) => {
    opsi.addEventListener("click", () =>  {
        id = opsi.id.charAt(opsi.id.length - 1)
        SetActivateContent(id)
    })
})