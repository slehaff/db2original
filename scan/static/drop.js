function renderRowCounter() {
  var rowCount = [25, 50, 100];
  var first = rowCount[0];
  var items = "";

  $.each(rowCount, function(i, v) {
    items += '<li><a href="#">' + v + "</a></li>";
  });

  return (
    '<div class="btn-group btn-group-sm">' +
    '<button type="button" data-toggle="dropdown" class="btn btn-default dropdown-toggle">' +
    first +
    ' <span class="caret"></span></button>' +
    '<ul class="dropdown-menu">' +
    items +
    "</ul>" +
    "</div> "
  );
}

$(document).ready(function() {
  $(".dropdown").on("show.bs.dropdown", function() {
    $.ajax({
      url: "../scan/drop/",
      type: "GET",
      success: function(cities) {
        console.log("console dropdown");
      },
      error: function() {
        console.log("error");
      }
    });
  });
  $(".dropdown").on("shown.bs.dropdown", function() {
    console.log("The dropdown is now fully shown.");
  });
  $(".dropdown").on("hide.bs.dropdown", function(e) {
    console.log("The dropdown is about to be hidden.");
  });
  $(".dropdown").on("hidden.bs.dropdown", function() {
    console.log("The dropdown is now fully hidden.");
  });
});
