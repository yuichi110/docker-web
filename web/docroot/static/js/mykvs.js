var refreshTable = function(){
  $.ajax({type:'get', url:'/api/v1/keys/', 
    success:function(j){
      $('#table').empty()
      var hline = '<tr><th scope="col">#</th><th scope="col">Key</th>'
      hline += '<th scope="col">Value</th></tr>'
      $('#table').append(hline)

      var index = 1
      for(var key in j){
        var line = '<tr><th scope="row">' + index + '</th>'
        line += '<td>' + key + '</td><td>' + j[key] + '</td></tr>'
        $('#table').append(line)
        index++
      }
    }
  })
}

$(function(){

  $('#get-button').click(function(){
    $.ajax({type:'get', url:'/api/v1/keys/'+$('#key').val(),
      success:function(j){
        alert(JSON.stringify(j, null, '  '))
      }, 
      error:function(d){
        alert(d.responseText)
      }
    })
  })

  $('#post-button').click(function(){
    $.ajax({type:'post', url:'/api/v1/keys/'+$('#key').val(), 
      data:$('#value').val(),
      success:function(j){
        refreshTable()
      }, 
      error:function(d){
        alert(d.responseText)
      }
    })
  })

  $('#put-button').click(function(){
    $.ajax({type:'put', url:'/api/v1/keys/'+$('#key').val(), 
      data:$('#value').val(),
      success:function(j){
        refreshTable()
      }, 
      error:function(d){
        alert(d.responseText)
      }
    })
  })

  $('#delete-button').click(function(){
    $.ajax({type:'delete', url:'/api/v1/keys/'+$('#key').val(),
      success:function(j){
        refreshTable()
      }, 
      error:function(d){
        alert(d.responseText)
      }
    })
  })

  $('#key').keyup(function(){
    var newText = 'URL: /api/v1/keys/' + $('#key').val()
    $('#key-text').text(newText)
  })

  $('#value').keyup(function(){
    var newText = 'Body: ' + $('#value').val()
    $('#value-text').text(newText)
  })

  refreshTable()
  setInterval(refreshTable, 5000)
})