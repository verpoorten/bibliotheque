
/*$("#lu" ).click(function(event) {

  var target = $(event.target);
  var id = target.attr("id");
  if (typeof id == 'undefined') {
    target = target.parent();
    id = target.attr("id");
  }

  alert(event.target.checked);

  if (typeof id != 'undefined') {

    link = id.replace(/-/g , "/");
    link =  link;
    alert(link);
      $.ajax({
        type: "POST",
        url: link,
        success: function(msg) {
          url = window.location.href.toString();
          url = url.replace("#", "");
          console.log(url);
          window.location.replace(url);
        }
      });

  }
});*/
