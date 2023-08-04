// // // window.onload = function() {
// // //         let things = document.getElementsByTagName("input")
// // //         const inputs = Array.from(things)
// // //         inputs.forEach(input => {
// // //                 input.addEventListener('keypress', () => {
// // //                        if(input.readOnly == true){
// // //                                alert("This is a readonly field")
// // //                        }
// // //                 })
// // //         })
// // //       };

// // alert("Hello") 


// // alert("Hello") 

const upFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}





// function getData(){

//         var requestOptions = {
//                 method: 'GET',
//                 redirect: 'follow'
//               };

//         var api_key='66d4824684db8ea0ab67fa76'
//         var amount = document.getElementById('unit_amount_usd').value

//         var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
//                 .then(response => response.json())
//                 .then(
//                         result => {
//                                 // var url = result.conversion_result
//                                 document.getElementById('unit_amount_ghs').value = result.conversion_result
//                         }
//                 )
//                 .catch(error => console.log('error', error));

// }





// function getSize(){

//         var myHeaders = new Headers();
//         myHeaders.append("Content-Type", "application/json");
//         myHeaders.append("Cookie", "csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ");
//         myHeaders.append("Access-Control-Allow-Origin", "*");
        
//         var client_id = document.getElementById('client_size').value

//         // alert(client_id)

//         var raw = JSON.stringify({
//           "client_id": client_id
//         });
        
//         var requestOptions = {
//           method: 'POST',
//           headers: myHeaders,
//           body: raw,
//           redirect: 'follow'
//         };
        
//         fetch("http://127.0.0.1:8000/api/client-size/", requestOptions)
//           .then(response => response.json())
//           .then(
//                 result => {
//                         console.log(result)
//                         // document.getElementById('modula').value = result.info.membership_size
//                 }
//                 )
//           .catch(error => console.log('error', error));

// }

const memberOut = () => {
        // alert("Hello")
        window.localStorage.removeItem('token');
    }
   



function addRen(){

        var renewing_days = document.getElementById('renewing_days')
        var expiring_days = document.getElementById('expiring_days')
        var remaining_days = document.getElementById('remaining_days')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('sub_duration')


        
        //alert(expiring_days.value)


        if(duration.value == ""){
            renewing_days.value = 0 * 30
            remaining_days.value = 0 - parseInt(expiring_days.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                renewing_days.value = parseInt(duration.value) * 30
                remaining_days.value = parseInt(renewing_days.value) - parseInt(expiring_days.value)
                special_unit_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
                special_unit_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)
        }
        
}  





function changesValue(){

        var renewing_days = document.getElementById('renewing_days')
        var expiring_days = document.getElementById('expiring_days')
        var remaining_days = document.getElementById('remaining_days')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('set_duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        var url = paymentForm.getAttribute("data-modula-url")

        
        // alert("Inside")

        if(duration.value == ""){
            renewing_days.value = 0 * 30
            remaining_days.value = 0 - parseInt(expiring_days.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                renewing_days.value = parseInt(duration.value)
                remaining_days.value = parseInt(renewing_days.value) - parseInt(expiring_days.value)
                special_unit_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
                special_unit_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)
        }
        
}  








function changedValue(){

        var renewing_days = document.getElementById('renewing_days')
        var expiring_days = document.getElementById('expiring_days')
        var remaining_days = document.getElementById('remaining_days')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('set_duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        var url = paymentForm.getAttribute("data-modula-url")

        var per_day_usd = parseInt(unit_amount_usd.value) / 30
        var per_day_ghs = parseInt(unit_amount_ghs.value) / 30

        // alert(per_day_usd)
        // alert(per_day_ghs)

        // alert("Inside")

        if(duration.value == ""){
            renewing_days.value = 0 * 30
            remaining_days.value = 0 - parseInt(expiring_days.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                renewing_days.value = parseInt(duration.value)
                remaining_days.value = parseInt(renewing_days.value) - parseInt(expiring_days.value)


                special_unit_amount_usd.value = Math.round(parseInt(duration.value) * parseFloat(per_day_usd))
                special_unit_amount_ghs.value = Math.round(parseInt(duration.value) * parseFloat(per_day_ghs))
        }
        
}  





const downFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}


const checkOut = (event) => {
        const expire = document.getElementById('expire')

        if(event.checked == false){
                expire.style.display = "block"
        }
        else{
                expire.style.display = "none"
        }
        
}

const changeValue = () => {
        const duration = document.getElementById('set_duration')
        const unit_amount_usd = document.getElementById('unit_amount_usd')
        const unit_amount_ghs = document.getElementById('unit_amount_ghs')
        const total_amount_usd = document.getElementById('total_amount_usd')
        const total_amount_ghs = document.getElementById('total_amount_ghs')

        total_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
        total_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)

}



const addValue = () => {
        const promo_discount = document.getElementById('promo_discount')
        const total_amount_usd = document.getElementById('special_unit_amount_usd')
        const total_amount_ghs = document.getElementById('special_unit_amount_ghs')
        const amount_usd = document.getElementById('amount_usd')
        const amount_ghs = document.getElementById('amount_ghs')

        // promo_discount
        // amount_usd
        // amount_ghs

        amount_usd.value = parseInt(total_amount_usd.value) - ((parseInt(promo_discount.value) * 0.01) * parseInt(total_amount_usd.value))
        amount_ghs.value = parseInt(total_amount_ghs.value) - ((parseInt(promo_discount.value) * 0.01) * parseInt(total_amount_ghs.value))
        // amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)

}




const getFile = () => {

        const signature = document.getElementById('signature')
        const signaturePreview = document.getElementById('signature-preview')
        const previewImage = document.querySelector(".image")
        const previewTextDefault = document.querySelector(".default-text")

        signature.addEventListener('change', function() {
                const file = this.files[0];
                
        
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        signaturePreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        signaturePreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}


const getLogo = () => {

        const logo = document.getElementById('logo')
        const logoPreview = document.getElementById('logo-preview')
        const previewImage = document.querySelector(".logo-image")
        const previewTextDefault = document.querySelector(".logo-text")

        logo.addEventListener('change', function() {
                const file = this.files[0];
                
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        logoPreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        logoPreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}







function showDur(){
        dur = document.getElementById('dur')
        subscription_type = document.getElementById('subscription_type')

        
        if(subscription_type.value == "Account Activation"){
                dur.style.display= 'block';
        }
        else if(subscription_type.value == "Module Subscription"){
                dur.style.display= 'none';

        }
        else{
                dur.style.display= 'none';
        }
}


function pullDisc(source){
        disc = document.getElementById('disc')

        if (source.checked == true){
                disc.style.display = 'block';
        }
        else{
                disc.style.display = 'none';
        }
}


function toggle(source) {
        checkboxes = document.getElementsByName('foo[]');
        inputs = document.getElementsByName('foo[]');
        database = document.getElementById('default');

        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = source.checked;
        }

        database.checked = true;
      }


// function toggle(source) {
//         var checkboxes = document.getElementsByName('foo[]');
//         var database = document.getElementById('default');
      
//         for (var i = 0, n = checkboxes.length; i < n; i++) {
//           if (database.checked) {
//             // do nothing if checkbox is already checked and source is being unchecked
//           } else {
//             checkboxes[i].checked = source.checked;
//           }
//         }
//       }
      



const softCheck = () => {
        for(let i=1; i<100; i++){
                // let radio = document.getElementById("subject"+i)
                // let period = document.getElementById("module"+i)

                if(document.getElementById("subject"+i).checked){
                        document.getElementById("module"+i).disabled = false 

                }
                else{
                        document.getElementById("module"+i).disabled = true 
                }
                }
} 




const checkAmount = (e) => {
        var checked_values = []

        var selected_value = [];

        var sources = document.getElementsByClassName("source");

        Array.prototype.forEach.call(sources, function(e){
                if(e.checked){
                        selected_value.push(e.getAttribute("data-id"))
                        document.getElementById("duration"+e.getAttribute("data-id")).disabled = false;
                }else{
                        document.getElementById("duration"+e.getAttribute("data-id")).disabled = true;
                }
        });
}



const changeDur = (event) => {

        var day = document.getElementById("day");
        var month = document.getElementById("month");
        // var dur_type = document.getElementsById("dur_type");
        
        // alert(event.value)
        
        if(event.value == "days"){
                day.style.display = null;
                month.style.display = 'none';
        }else{
                day.style.display = 'none';
                month.style.display = null;     
        }
}



const changeAmount = (e) => {
        var checked_values = []

        var selected_value = [];

        var sources = document.getElementsByClassName("source");

        Array.prototype.forEach.call(sources, function(e){
                if(e.checked){
                        selected_value.push(e.getAttribute("data-id"))
                        // alert(e.getAttribute("data-id"))
                        document.getElementById("unit_amount_usd"+e.getAttribute("data-id")).disabled = false;
                        document.getElementById("unit_amount_ghs"+e.getAttribute("data-id")).disabled = false;
                        document.getElementById("unit_amount_usd"+e.getAttribute("data-id")).required = true;
                        document.getElementById("unit_amount_ghs"+e.getAttribute("data-id")).readOnly = true;
                }else{
                        document.getElementById("unit_amount_usd"+e.getAttribute("data-id")).disabled = true;
                        document.getElementById("unit_amount_ghs"+e.getAttribute("data-id")).disabled = true;
                }
        });
}


function getReal(){

        var requestOptions = {
                method: 'GET',
                redirect: 'follow'
              };

        var api_key='66d4824684db8ea0ab67fa76'
        var amount = document.getElementById('special_subscription_fee_usd').value

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                document.getElementById('special_subscription_fee_ghs').value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

}



function getMain(){

        var requestOptions = {
                method: 'GET',
                redirect: 'follow'
              };

        var api_key='66d4824684db8ea0ab67fa76'
        var amount = document.getElementById('maintenance_fee_usd').value

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                document.getElementById('maintenance_fee_ghs').value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

}



function getData(e){

        amount_ghs = document.getElementById("unit_amount_ghs"+e.getAttribute("data-id"))

        var requestOptions = {
        method: 'GET',
        redirect: 'follow'
                };

        var api_key='e660c7f73ca24b041ceee820'
        var amount = e.value

        if(amount == ""){
                amount=0 
        } 

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                amount_ghs.value = (result.conversion_result).toFixed(2)
                                // amount_ghs.value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

        
}







function get2Data(e){

        amount_ghs = document.getElementById("unit_amount_ghs")

        var requestOptions = {
        method: 'GET',
        redirect: 'follow'
                };

        var api_key='e660c7f73ca24b041ceee820'
        var amount = e.value

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                amount_ghs.value = (result.conversion_result).toFixed(2)
                                // amount_ghs.value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

        
}



function checkUsd(){


        var amount_usd = document.getElementsByClassName("unit_amounts_usd")[0].value
        var new_amount_usd = document.getElementById("unit_amount_usd").value
        

        if(new_amount_usd == ""){
                new_amount_usd = 0
        }
        
        if(parseInt(new_amount_usd) < parseInt(amount_usd)){
                alert("You cannot set below the original amount");
                
                document.getElementById("unit_amount_ghs").value = ""
                document.getElementById("unit_amount_usd").value = ""
        }

        
}


function checkActive(){

        // var element = document.getElementsByClassName("my-class")[0]

        var activation_fee = document.getElementById("activation_fee").value
        var agent_activation_fee = document.getElementById("agent_activation_fee").value
        

        if(agent_activation_fee == ""){
                agent_activation_fee = 0
        }
        
        if(parseInt(agent_activation_fee) < parseInt(activation_fee)){
                alert("You cannot set below the original amount");
                
                document.getElementById("agent_activation_fee").value = ""
        }

        
}








const changeRegion = (event) => {

        let stateProvince = document.getElementById('stateProvince')
        let region = document.getElementById('region')
        let district = document.getElementById('district')
        let constituency = document.getElementById('constituency')


        //alert(event.value)

        if(event.value == 76){
                //alert("Ghana"); 
                region.disabled = false;
                district.disabled = false;
                constituency.disabled = false; 
                stateProvince.disabled = true; 
                
        }else{
                region.disabled = true;
                district.disabled = true;
                constituency.disabled = true; 
                stateProvince.disabled = false;  
        }

}



 
      
function showMain(e){

        var maint = document.getElementById('maint')

        if(e.checked){
                maint.style.display = "block"
        }
        else{
                maint.style.display = "none"
        }
}      
