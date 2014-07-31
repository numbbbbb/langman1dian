/*
 * jQuery cursorHover
 * Copyright 2010 Jake Lauer with Clarity Design (isthatclear.com)
 * Released under the MIT and GPL licenses.
 */
		(function($){
			$.btn4.cursorHover = function(options) {

				var defaults = {
					outerImage: "",
					innerImage: "",
					fadeSpeed: 300,
					innerBorder:0,
					align: "bottom",
					zalign: "bottom"
				};

				var options = $.extend(defaults, options);

				return this.each(function() {

					//Set background image to specified image
					$(this).wrap('<div class="innerImage">');
					var innerDiv = $('.innerImage');


					var wfBorder = innerDiv.width() - ( options.innerBorder * 2 );
					var hfBorder = innerDiv.height() - ( options.innerBorder * 2 );
					
					//Check if it's linked
					if ( $(this).find('a') ) {
						var linkExists = true;
						var linkText = $(this).find('a').text(); //Keep SEO linking
						linkText = linkText.replace(linkText, '<span style="display:block;height:0px;overflow:hidden;">' + linkText + '</span>');
						var linkHTML = $(this).find('a').append( $(this).find('a').clone() ).remove().html();
						linkHTML = linkHTML.replace('</a>', '').replace('>','/>');
					}
					
					//Set inner image to specified image
					$(this).html('<img class="aInner" src="' + options.innerImage + '"/>');
					$(this).append('<img class="aTop" src="' + options.outerImage + '"/>');
					if ( linkExists == true ) {
						$(this).find('.aTop').wrap(linkHTML);
						$(this).find('a').append(linkText);
					}
					$(this).css({position:"relative"});
					var aInner = $('.aInner');
					var aTop = $('.aTop');
					
					switch (options.zalign)
					{
					case "bottom":
						var innerImageZ = 0;
						var outerImageZ = 0;
						break;
					case "top":
						var innerImageZ = 1;
						var outerImageZ = 2;
						break;
					}
					
					aInner.wrap('<div class="border">');
					$('.border').css({position:"absolute",top: options.innerBorder,left:options.innerBorder,width: wfBorder, height: hfBorder,overflow: "hidden", zIndex:innerImageZ});
					aInner.css({opacity:0, zIndex:outerImageZ});
					aTop.css({position:"absolute", top:0, left:0});
					
					switch (options.align)
					{
					case "bottom":
						alignment = ( innerDiv.height() - aInner.height() );
						break;
					case "center":
						alignment = ( innerDiv.height() - aInner.height() ) / 2;
						break;
					case "top":
						alignment = 0;
						break;
					}
					aInner.css({marginTop: alignment });

					//Center inner image inside outer image
					if (aInner.width() > $(this).width()) {
						aInner.css({
							marginLeft: ( aInner.width() - $(this).width() ) / -2
						});
					} else {
						aInner.css({
							marginLeft: ( $(this).width() - aInner.width() ) / 2
						});
					}

					//Fade on mouse over
					$(this).mouseenter(function(){
						aInner.stop().animate({
							opacity: 1
						}, options.fadeSpeed);
					});

					$(this).mousemove(function(e){
						var left = (e.pageX - $(this).offset().left - ( aInner.width() /2 ) );
						if ( left >= 0 ) {
							left = 0;
						}
						if ( ( left * -1 ) >= ( aInner.width() - innerDiv.width() ) ) {
							left = ( ( aInner.width() - innerDiv.width() ) * -1 );
						}
						aInner.css({marginLeft: left})
					});

					//Fade out on mouse leave
					$(this).mouseleave(function(){
						aInner.stop().animate({
							opacity: 0
						}, options.fadeSpeed);
					});
				});

				function extractUrl(input) {
					return input.replace(/"/g,"").replace(/url\(|\)$/ig, "");
				}
			};

		})(jQuery);