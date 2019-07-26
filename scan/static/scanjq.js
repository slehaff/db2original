$(document).ready(function() {
  $("#scan").on("click", function() {
    $.ajax({
      url: "../scan/scan/",
      type: "GET",
      success: function() {
        console.log("streaming");
      },
      error: function() {
        console.log("error");
      }
    });
  });

  $("#train").on("click", function() {
    $.ajax({
      url: "../scan/train/",
      type: "GET",
      success: function() {
        console.log("train scan");
      },
      error: function() {
        console.log("error");
      }
    });
  });

  $("#traindata").on("click", function() {
    $.ajax({
      url: "../scan/traindata/",
      type: "GET",
      success: function() {
        console.log("train data");
      },
      error: function() {
        console.log("error");
      }
    });
  });

  $("#phase24").on("click", function() {
    $.ajax({
      url: "../scan/ph24/",
      type: "GET",
      success: function() {
        console.log("streaming");
      },
      error: function() {
        console.log("error");
      }
    }).done(function() {
      $("#phaseimage")
        .attr("src", folder + "/image1.png")
        .delay(600)
        .fadeIn(400, function() {
          $("#phaseimage")
            .attr("src", folder + "/image2.png")
            .delay(600)
            .fadeIn(400, function() {
              $("#phaseimage").attr("src", folder + "/image3.png");
            });
        });
    });
  });

  $("#reference").on("click", function() {
    $.ajax({
      url: "../scan/reference/",
      type: "GET",
      success: function() {
        console.log("reference");
      },
      error: function() {
        console.log("error");
      }
    });
  });

  $("#unwrap").on("click", function() {
    $.ajax({
      url: "../scan/unw/",
      type: "GET",
      success: function() {
        console.log("streaming");
      },
      error: function() {
        console.log("error");
      }
    }).done(function() {
      $("#phaseimage").attr("src", folder + "/unwrap.png");
    });
  });

  $("#gamma").on("click", function() {
    $.ajax({
      url: "../scan/gamma/",
      type: "GET",
      success: function() {
        console.log("gamma");
      },
      error: function() {
        console.log("error");
      }
    });
  });
});
