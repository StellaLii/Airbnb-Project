// animation function for scrolling down the page
const navLinks = document.querySelectorAll("nav ul li a");
// console.log(navLinks)
for (const link of navLinks) {
  link.addEventListener("click", clickHandler);
}
function clickHandler(e) {
  e.preventDefault();
  const href = this.getAttribute("href");
  const offsetTop = document.querySelector(href).offsetTop;

  scroll({
    top: offsetTop,
    behavior: "smooth"
  });
}


$('#submit-1').click(function(){ 
  // fetching form data
  var formData = {
        Postal_Code: document.getElementById("postal-code").value,
        Property_Type: document.getElementById("property-type").value,
        Room_Type: document.getElementById("room-type").value,
        Accommodates: document.getElementById("accommodates").value,
        Bedroom_Num: document.getElementById("bedroom-num").value,
        Bed_Num: document.getElementById("bed-num").value,
        BBQ: $("#BBQ").is(':checked'),
        TV: $("#TV").is(':checked'),
        White_Goods: $("#white-goods").is(':checked'),
        Bathroom_Type: document.getElementById("bathroom-type").value,
        Bathroom_Num: document.getElementById("bathroom-num").value
  }

  $.ajax({ 
       // method
       type: "POST",
       // content-type
       contentType: "application/json",
       // payload
       data: JSON.stringify(formData),
       // endpoint url
       url: "your api gateway url",
       // on success
       success: function(data){        
          console.log("Success", data);
          const result_text = document.getElementById("result-text");
          result_text.textContent = data["result"];
          const status_1 = document.getElementById("status-text-1");
          status_1.textContent = data["result_status_1"];
          const status_2 = document.getElementById("status-text-2");
          status_2.textContent = data["result_status_2"];
         
       },
       // on error
       error: function(data){        
          console.log("Error", data);
       }
   });
});



$('#submit-2').click(function(){ 
  // fetching form data
  var formData = {
        Postal_Code: document.getElementById("postal-code-2").value,
        Price: document.getElementById("price").value,
        Host_Listing: document.getElementById("host-listing").value,
        Electronicss: $("#electronicss").is(':checked'),
        Bed_Linen: $("#bed-linen").is(':checked'),
        Coffee_Machine: $("#coffee-machine").is(':checked'),
        Cooking_Basics: $("#cooking-basics").is(':checked'),
        Child_Friendly: $("#child-friendly").is(':checked'),
        Parking: $("#parking").is(':checked'),
        Outdoor_Space: $("#outdoor-space").is(':checked'),
        Internet: $("#internet").is(':checked')
  }

  $.ajax({ 
       // method
       type: "POST",
       // content-type
       contentType: "application/json",
       // payload
       data: JSON.stringify(formData),
       // endpoint url
       url: "your api gateway url",
       // on success
       success: function(data){        
          console.log("Success", data);
          const result_text = document.getElementById("result-text-2");
          result_text.textContent = data["result"];
         
       },
       // on error
       error: function(data){        
          console.log("Error", data);
       }
   });
});