$(document).ready(function(){ 

	$(".contactArea").css('height', '0px');

	$("#contact").toggle( 
				function () { 
				if ($("#contactArea2").css("height")=="350px"){
				$("#contactArea2").animate({height: "0px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'}) 
				}
 					$("#contactArea1").animate({height: "225px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'}) 
                }, 
                function () { 
					$("#contactArea1").animate({height: "0px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'})  
				} 
		); 
		$("#contact1").toggle( 
	
				function () { 
				if ($("#contactArea1").css("height")=="225px"){
				$("#contactArea1").animate({height: "0px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'}) 
				}
 					$("#contactArea2").animate({height: "350px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'}) 
                }, 
                function () { 
					$("#contactArea2").animate({height: "0px"}, {queue:false, duration: 1700, easing: 'easeOutBounce'})  
				} 
		);
        
}); 
