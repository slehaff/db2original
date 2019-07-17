$(document).ready(function() {

  $('#take').on('click', function() {
    $.ajax({
    url: '../calibrate/take/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    })
  })



  $('#camcalib').on('click', function() {
    $.ajax({
    url: '../calibrate/camera/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    })
  })

  $('#wilm').on('click', function() {
    $.ajax({
    url: '../calibrate/wilm/',
    type: 'GET',
    success: function(){
      console.log('wilm')
    }, error: function(){
      console.log('error')
    }
    })
  })



  $('#phase1').on('click', function() {
    $.ajax({
    url: '../calibrate/ph1/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    }).done(function() {
    $("#phaseimage").attr("src", folder + 'ph10.jpg').delay(600).fadeIn(400, function() {
      $("#phaseimage").attr("src", folder + 'ph11.jpg').delay(600).fadeIn(400, function(){
      $("#phaseimage").attr("src", folder + 'ph12.jpg')
      })
    })
  });
  })

  $('#phase24').on('click', function() {
    $.ajax({
    url: '../calibrate/ph24/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    }).done(function() {
    $("#phaseimage").attr("src", folder + 'ph240.jpg').delay(600).fadeIn(400, function() {
      $("#phaseimage").attr("src", folder + 'ph241.jpg').delay(600).fadeIn(400, function(){
      $("#phaseimage").attr("src", folder + 'ph242.jpg')
      })
    })
  });
  })

  $('#wrap').on('click', function() {
    $.ajax({
    url: '../calibrate/wrap/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    })
  })

  $('#unwrap').on('click', function() {
    $.ajax({
    url: '../calibrate/unw/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
  }).done(function(){
    $("#phaseimage").attr("src", folder + 'unwrap.jpg')
  })
  })

  $('#pose').on('click', function() {
    $.ajax({
    url: '../calibrate/pose/',
    type: 'GET',
    success: function(){
      console.log('pose')
    }, error: function(){
      console.log('error')
    }
    })
  })

  $('#projector').on('click', function() {
    $.ajax({
    url: '../calibrate/pro/',
    type: 'GET',
    success: function(){
      console.log('projector')
    }, error: function(){
      console.log('error')
    }
    })
  })

  $('#newscan').on('click', function() {
    $.ajax({
    url: '../calibrate/newscan/',
    type: 'GET',
    success: function(){
      console.log('streaming')
    }, error: function(){
      console.log('error')
    }
    })
  })

});
