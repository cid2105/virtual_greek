
/*
	jPoll jQuery plugin version 1.0
	
	Copyright (c) 2009 Dan Wellman
  
	Dual licensed under the MIT and GPL licenses:
  http://www.opensource.org/licenses/mit-license.php
  http://www.gnu.org/licenses/gpl.html
	
*/

(function($) {
	
	//define jPoll object with some default properties
	$.jPoll = {
		defaults: {
			ajaxOpts: {
				url: "poll"
			},
			groupName: "choices",
			groupIDs: ["choice0", "choice1", "choice2", "choice3", "choice4"],
			pollHeading: "Please choose your favourite:",
			rowClass: "row",
			errors: true
		}
	};
  
	//extend jquery with the plugin
	$.fn.extend({
		jPoll:function(config) {
																
			//use defaults or properties supplied by user
			config = $.extend({}, $.jPoll.defaults, config);
			
			//init widget
			$("<h2>").text(config.pollHeading).appendTo($(this));
			$("<form>").attr({
				id: "pollForm",
				action: config.ajaxOpts.url
		  }).appendTo($(this));
			for(var x = 0; x < config.groupIDs.length; x++) {
				$("<div>").addClass(config.rowClass).appendTo($(this).find("form"));
				$("<input type='radio' name='" + config.groupName + "' id='" + config.groupIDs[x] + "'>").addClass("choice").appendTo($(this).find("form").children(":last")).click(function() {
					($(".error").length != 0) ? $(".error").slideUp("slow") : null ;
				});
				$("<label>").text(config.groupIDs[x]).attr("for", config.groupIDs[x]).appendTo($(this).find("form").children(":last"));
			}
			$("<div>").attr("id", "buttonRow").addClass(config.rowClass).appendTo($(this).find("form"));
			$("<button type='submit'>").text("Vote!").appendTo("#buttonRow").click(function(e) {
				e.preventDefault();
				
				//record which radio was selected
				var selected;
				$(".choice").each(function() {
					($(this).attr("checked") == true) ? selected = $(this).attr("id") : null ;
				});
				
				//print message if no radio selected and errors enabled
				if (config.errors == true) {
					(selected == null && $(".error").length == 0) ? $("<p>").addClass("error").text("Please make a selection!").css({display:"none"}).insertAfter("#pollForm").slideDown("slow") : null ;
				}
				
				//add additional request options
				var addOpts = {
					type: "post",
					data: "&choice=" + selected,
					dataType:"json",
					success: function(data) {
		
						//add all votes to get total
						var total = 0;
							for (var x = 0; x < data.length; x++) {
							total += parseInt(data[x].votes);
						}
						//change h2
						$("div#pollContainer").find("h2").text("Results, out of " + total + " votes:");
										
						//remove form
						$("form#pollForm").slideUp("slow");
						
						//create results container
						$("<div>").attr("id", "results").css({ display:"none" }).insertAfter("#pollForm");
										
						//create results
						for (var x = 0; x < data.length; x++) {
							
							//create row elment
							$("<div>").addClass("row").attr("id", "row" + x).appendTo("#results");
							
							//create label and result
							$("<label>").text(config.groupIDs[x]).appendTo("#row" + x);
							$("<div>").attr("title", Math.round(data[x].votes / total * 100) + "%").addClass("result").css({ display:"none" }).appendTo("#row" + x);
						}
						
						//show results container
						$("#results").slideDown("slow", function() {
						
							//animate each result
							$(".result").each(function(i) {
								$(this).animate({ width: Math.round(data[i].votes / total * 100) }, "slow");
							});	
							
							//create and show thanks message
							$("<p>").attr("id", "thanks").text("Thanks for voting!").css({ display:"none" }).insertAfter("#results").fadeIn("slow");		
						});							
					}
				};
				//merge ajaxOpts widget properties and additional options objects
				ajaxOpts = $.extend({}, addOpts, config.ajaxOpts);
				
				//make request if radio selected
				return (selected == null) ? false : $.ajax(ajaxOpts) ;
			});
			
			//return the jquery object for chaining
			return this;
		}
  });
})(jQuery);

