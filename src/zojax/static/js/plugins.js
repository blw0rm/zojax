
// remap jQuery to $
(function($){
    $.fn.showPopup = function(clear_parent) {
        /*
        * Create pop-up window.
        * */
	    var href = this.attr("href");
	    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
	    win.focus();
	    if (clear_parent)
	    win.opener = null;
	    return false;
	};

    $.fn.loadIndicator=function(){
        var loader=$('<div class="loader"></div>');
        loader.height($(this).parent().height());
        loader.width($(this).parent().width());

        return $(this).before(loader).addClass('ajax-loading');
    };

    $.fn.deleteIndicator = function() {
    	/*
    	 * Delete loader indicator
    	 */
    	$(this).removeClass('ajax-loading').prev('div.loader').remove();
    };

})(this.jQuery);

$(function(){
   /*
   * Process ajax logout.
   * */
   $(".account-wrapper #logout").live("click", function(){
        $.get($(this).attr("href"), function(data, textStatus, jqXHR) {
            data = $(data);
            $("#account-box").html(data.find("#account-box").html());
            $("#main").html(data.find("#main").html());

        });
        return false;
   });
});

function bindShare(data, status, xhr, $form) {
    var wrapper = $form.parents(".formwrapper");
    if (data) {
        wrapper.html(data);
        wrapper.find("form").ajaxForm({
            success:   bindShare  // post-submit callback
        });
    }
}

function bindExtra(data, status, xhr, $form) {
    var wrapper = $form.parents(".formwrapper"),
        jdata = $(data);
    var openid_form = jdata.find(".openid form");
    if (openid_form.length > 0) {
        wrapper.html('');
        wrapper.append(openid_form);
        wrapper.find("form").ajaxForm({
            success:   bindExtra  // post-submit callback
        });
    } else { /* We are on main page */
        $("#account-box").html(jdata.find("#account-box").html());
        $("#main").html(jdata.find("#main").html());
        $("div.upload form").ajaxForm({
            success:    bindUpload,  // post-submit callback
            dataType:  "json"        // 'xml', 'script', or 'json' (expected server response type)
        });
    }
}

function bindUpload(data, status, xhr, $form) {
    var wrapper = $form.parents(".formwrapper"),
        doclist = $("ul.doclist");
    $form.deleteIndicator();
    if (data) {
        wrapper.html(data.form);
        if (data.document) {
            doclist.append(data.document);
        }
        wrapper.find("form").ajaxForm({
            beforeSubmit: function(arr, $form, options) {
                $form.loadIndicator();
            },
            success:   bindUpload,  // post-submit callback
            dataType:  "json"        // 'xml', 'script', or 'json' (expected server response type)
        });
    }
}


// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};



// catch all document.write() calls
(function(doc){
  var write = doc.write;
  doc.write = function(q){ 
    log('document.write(): ',arguments); 
    if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);  
  };
})(document);


