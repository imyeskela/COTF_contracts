require('bootstrap');

function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}

document.addEventListener('DOMContentLoaded', function(){
    let phone_input = document.getElementById("id_phone");
    if(phone_input){
        let phone = phone_input.value;
        if(phone.substring(0,2) != "+7"){
            phone_input.value = "+7";
        }
        phone_input.addEventListener("input",function(e){
            let phone = this.value;
            if(phone.substring(0,2) != "+7"){
                phone_input.value = "+7";
            }
        })
    }
    let contract_client_form = document.getElementById("contract_client_form");
    document.querySelectorAll(".tr_contract").forEach(function (tr){
        tr.querySelectorAll(".dropdown").forEach(function (dropdown){
            dropdown.querySelectorAll(".dropdown-item").forEach(function (item){
                item.addEventListener("click",function (){
                    let input = dropdown.querySelector("input");
                    input.value = capitalize(this.innerText.toLowerCase());
                    let form = document.getElementById("contract_update_form");
                    let pk_input = tr.querySelector("input[name='contract_template_pk']");
                    form.appendChild(input);
                    form.appendChild(pk_input);
                    form.submit();
                });
            })
        });
        let url_copy_btn = tr.querySelector(".url_copy_btn")
        url_copy_btn.addEventListener("click",function (e){
            if (url_copy_btn.dataset.status === 'Актуально') {
                let data = {"create_contract" : true};
                data.identifier = tr.querySelector("input[name='identifier']").value;
                data.amount = tr.querySelector("input[name='amount']").value;
                data.pk = tr.querySelector("input[name='contract_template_pk']").value;
                data.csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                xrhPost(window.location,data,function (response) {
                    let contract_number = response.contract_number;
                    let contract_url = window.location.origin + '/agreement/' + contract_number + '/';
                    copy_url(tr, contract_url);
                });
            }
        });
    });
    document.querySelectorAll(".tr_contracts_client").forEach(function (tr) {
        let pk = tr.dataset.contractNumber;
        let url_copy_btn = tr.querySelector(".url_copy_btn");
        let url = window.location.origin + "/agreement/" + pk + "/";
        url_copy_btn.querySelector("input[name='contract_url']").value = url;
        url_copy_btn.addEventListener("click",function () {
            copy_url(tr,url);
        })
        tr.querySelectorAll(".status_box").forEach(function (status_box) {
            status_box.querySelector(".icon-more").addEventListener("click",function () {
                document.querySelectorAll(".status_box").forEach(function (item) {
                    item.querySelector(".cancel").classList.remove("show");
                })
                let cancel = status_box.querySelector(".cancel");
                cancel.classList.add("show");
                cancel.addEventListener("click",function () {
                    let input_pk = document.createElement("input");
                    input_pk.setAttribute("name","pk");
                    input_pk.setAttribute("value",pk);
                    let input_status = document.createElement("input");
                    input_status.setAttribute("name","status");
                    input_status.setAttribute("value","Отказ");
                    contract_client_form.appendChild(input_pk);
                    contract_client_form.appendChild(input_status);
                    contract_client_form.submit();
                })
            })
        })
        tr.querySelector(".download_button").addEventListener("click",function () {
            let input_pk = document.createElement("input");
            input_pk.setAttribute("name","pk");
            input_pk.setAttribute("value",pk);
            let input_download = document.createElement("input");
            input_download.setAttribute("name","download_contract");
            input_download.setAttribute("value",true);
            contract_client_form.appendChild(input_pk);
            contract_client_form.appendChild(input_download);
            contract_client_form.submit();
        })
    })
});

function xrhPost(url,data,f) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader("X-CSRFToken",data.csrfmiddlewaretoken);
    xhr.onreadystatechange = function() {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            console.log(xhr.response);
            response = JSON.parse(xhr.response);
            f(response);
        }
    }
    //console.log(JSON.stringify(data));
    xhr.send(JSON.stringify(data));
}

if(document.getElementById("paint")){
    let tab_pane = document.querySelectorAll(".tab-pane").forEach(function (item){
        if(item.clientWidth > 0){
            document.getElementById("paint").setAttribute("width",item.clientWidth);
        }
    })
    let c = new fabric.Canvas('paint');
    c.isDrawingMode = true;
    c.freeDrawingBrush.width = 3;
    c.freeDrawingBrush.color = "#000";
    document.querySelector("#clearCanvas").addEventListener("click",() => {
        c.clear();
    })
    document.getElementById("signContract").addEventListener("click",() => {
        document.getElementById("sign").value = document.getElementById("paint").toDataURL('image/jpeg', 1.0)
    })
}

function copy_url(elem, url) {
    let contract_url_input = elem.querySelector("input[name=contract_url]")
    contract_url_input.value = url;
    contract_url_input.select();
    navigator.clipboard.writeText(contract_url_input.value);
    let alert = elem.querySelector(".alert");
    alert.classList.add("show");
    setTimeout(function () {
        alert.classList.remove("show");
    },1500);
}

let modal = document.getElementById("contract_add_modal");
if(modal){
    let template_of_contract = document.getElementById('id_template_of_contract');
    let file_label = document.querySelector("label[for='id_template_of_contract']");
    if(template_of_contract){
        template_of_contract.onchange = function () {
            let file_name = this.value.split("\\").pop();
            file_label.innerText = file_name;
        };
    }
    let form = modal.querySelector("form");
    modal.querySelector(".refresh").addEventListener("click",function () {
        form.querySelector("input#id_check_file").value = true;
        form.querySelector(".buttons .btn_grd").click();
    })
    modal.querySelector(".clear").addEventListener("click",function () {
        template_of_contract.value = "";
        file_label.innerText = "+ Загрузить договор";
    })
}

let acceptButton = document.getElementById('acceptButton');
if(acceptButton){
    acceptButton.addEventListener('click', function (e) {
        document.querySelectorAll(".nav-link").forEach(function (item,i){
            if(i == 2){
                item.classList.add('active');
            }else{
                item.classList.remove('active')
            }
        })
        document.querySelectorAll(".tab-pane").forEach(function (item,i){
            if(i == 2){
                item.classList.add('active');
                item.classList.add('show');
            }else{
                item.classList.remove('active');
                item.classList.remove('show');
            }
        });
    })
}

let timer = document.getElementById("timer");
if(timer){
    let seconds = parseInt(timer.innerText);
    let interval = setInterval(function (){
        seconds--;
        if(seconds === 0){
            clearInterval(interval);
            document.querySelector(".btn_new_code").removeAttribute("disabled");
            timer.parentElement.remove();
        }
        timer.innerText = seconds;
    },1000);
}

let wizard = document.getElementById("wizard");
if(wizard){
    wizard.querySelectorAll(".nav-link").forEach(function (item,i){
        item.setAttribute("data-bs-toggle","tab");
        item.setAttribute("data-bs-target","#nav-" + (i+1));
        if(item.classList.contains("active")) {return;}
    })
}
