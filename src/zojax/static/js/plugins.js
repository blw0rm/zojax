
// remap jQuery to $
(function($){

 





 



})(this.jQuery);

function bindShare(data, status, xhr, $form) {
    var wrapper = $form.parents(".formwrapper");
    if (data) {
        wrapper.html(data);
        wrapper.find("form").ajaxForm({
            success:   bindShare  // post-submit callback
        });
    }
}

function bindUpload(data, status, xhr, $form) {
    var wrapper = $form.parents(".formwrapper"),
        doclist = $("ul.doclist");

    if (data) {
        wrapper.html(data.form);
        if (data.document) {
            doclist.append(data.document);
        }
        wrapper.find("form").ajaxForm({
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


