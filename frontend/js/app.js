require('bootstrap');

function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}

document.addEventListener('DOMContentLoaded', function(){
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
            let data = {"create_contract" : true};
            data.identifier = tr.querySelector("input[name='identifier']").value;
            data.amount = tr.querySelector("input[name='amount']").value;
            data.pk = tr.querySelector("input[name='contract_template_pk']").value;
            data.csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            xrhPost(window.location,data,function (response) {
                let contract_number = response.contract_number;
                let contract_url = window.location.origin + '/agreement/' + contract_number + '/';
                copy_url(tr,contract_url);
            });
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

//function makeContractUpdateForm(tr) {
//    let form = document.getElementById("contract_update_form");
//    tr.querySelectorAll("input").forEach(function (input) {
//        form.appendChild(input);
//    })
//    form.submit();
//}

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
    let c = new fabric.Canvas('paint');
    c.isDrawingMode = true;
    c.freeDrawingBrush.width = 3;
    c.freeDrawingBrush.color = "#000";
    document.querySelector(".clear_convas").addEventListener("click",() => {
        c.clear();
    })
    // document.querySelector("BUTTON").addEventListener("click",() => {
    //     let input = document.querySelector("INPUT").value =
    //     document.getElementById("paint").toDataURL('image/jpeg', 1.0)
    // })

}


// let wizard = {
//     wizard_elem: document.getElementById("wizard"),
//     page: 1,
//     next:function(){
//         this.page++;
//         this.wizard_elem.querySelectorAll(".tab-pane").forEach(function (item) {
//             item.classList.remove("show");
//             item.classList.remove("active");
//         })
//         this.wizard_elem.querySelector("#nav-"+this.page).classList.add("show");
//         this.wizard_elem.querySelector("#nav-"+this.page).classList.add("active");
//         this.wizard_elem.querySelectorAll(".nav-link").forEach( (item) => {
//             item.classList.remove("active");
//         })
//         this.wizard_elem.querySelector("#nav-"+this.page+"-tab").classList.add("active");
//     },
//     makeSignature: function () {
//
//     },
//     init:function () {
//         if(this.wizard_elem){
//             this.makeSignature();
//             this.wizard_elem.querySelectorAll(".btn_next").forEach( (button) => {
//                 button.addEventListener("click", () => {
//                     this.next();
//                 })
//             })
//         }
//         this.wizard_elem.querySelector(".btn_submit").addEventListener("click",() => {
//             this.makeForm()
//         })
//         this.wizard_elem.querySelector(".btn_send_sms").addEventListener("click",() => {
//             let data = {
//                 send_code: true,
//                 phone: this.wizard_elem.querySelector("#phone")
//             };
//             xrhPost(window.location,data,function (callback) {
//                 console.log(callback);
//             })
//         })
//         this.wizard_elem.querySelector(".btn_check_code").addEventListener("click",() => {
//             let data = {
//                 check_code: true,
//                 code: this.wizard_elem.querySelector("#code")
//             };
//             xrhPost(window.location,data,function (callback) {
//                 console.log(callback);
//             })
//         })
//     },
//     makeForm:function () {
//         let data = {
//             signature: this.wizard_elem.querySelector("#paint").toDataURL('image/jpeg', 1.0),
//             fname: this.wizard_elem.querySelector("#fname").value,
//             lname: this.wizard_elem.querySelector("#lname").value,
//             mname: this.wizard_elem.querySelector("#mname").value,
//             passport: this.wizard_elem.querySelector("#passport").value +
//                 this.wizard_elem.querySelector("#passport_num").value,
//             email: this.wizard_elem.querySelector("#email"),
//             phone: this.wizard_elem.querySelector("#phone"),
//         }
//         xrhPost(window.location,data,function (callback) {
//             console.log(callback);
//         })
//     },
//
// }
//
// wizard.init();


function copy_url(elem,url) {
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

let template_of_contract = document.getElementById('template_of_contract');
if(template_of_contract){
    template_of_contract.onchange = function () {
        let file_name = this.value.split("\\").pop();
        document.querySelector("label[for='template_of_contract']").innerText = file_name;
    };
}
