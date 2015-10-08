lasttime = '0' ;

updatechat();
updateusers();


 setInterval(function(){
 	updateusers();
 },2000);

setInterval(function(){
 	updatechat();
 },2000);

 function updateusers(){

 	var xmlhttp1=new XMLHttpRequest();

 	xmlhttp1.onreadystatechange=function()
	  {
	  if (xmlhttp1.readyState==4 && xmlhttp1.status==200)
	    {
	    document.getElementById("userlist").innerHTML=xmlhttp1.responseText;
	    }
	  }
 	xmlhttp1.open("GET","users",true);
	
	xmlhttp1.send();

 }


 function post(){
 	if (document.getElementById("posttext").value ==="")
 		return;

 	
 	var xmlhttp2=new XMLHttpRequest();
	
 	xmlhttp2.onreadystatechange=function()
	  {
	  if (xmlhttp2.readyState===4 && xmlhttp2.status===200)
	    {
	    	document.getElementById("posttext").value = "";
	    	updatechat();
	    }
	  }
 	xmlhttp2.open("POST","chat",true);
	xmlhttp2.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	params = "postcontent="+base64_encode(document.getElementById("posttext").value);
	xmlhttp2.send(params);

 }

function updatechat(){
	var xmlhttp=new XMLHttpRequest();

 	xmlhttp.onreadystatechange=function()
	  {
	  if (xmlhttp.readyState==4 && xmlhttp.status==200)
	    {
        var obj=JSON.parse(xmlhttp.responseText);
        lasttime = obj.time;
        var tmp = "";
        for (var i = 0; i < obj.posts.length; i++) {
          var post = obj.posts[i];
          tmp+='<div class="chat-box"><h4>'+post.user+'</h2><p>'+replaceAll('\n','<br>',  base64_decode(post.content))+'</p></div>\n';
        }
        var el =document.getElementById("chat");
        el.innerHTML = el.innerHTML + tmp;
        if(obj.posts.length>0)
  			 el.scrollTop = el.scrollHeight;
	    }
	  };
 	xmlhttp.open("GET","chat?lasttime="+lasttime,true);
	
	xmlhttp.send();
}

function initTime(){
  var xmlhttp=new XMLHttpRequest();

  xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
        lasttime=xmlhttp.responseText;
      el.scrollTop = el.scrollHeight;
      }
    }
  xmlhttp.open("GET","time",true);
  
  xmlhttp.send();
}

 function base64_encode(data) {
  //  discuss at: http://phpjs.org/functions/base64_encode/
  // original by: Tyler Akins (http://rumkin.com)
  // improved by: Bayron Guevara
  // improved by: Thunder.m
  // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // improved by: Rafał Kukawski (http://kukawski.pl)
  // bugfixed by: Pellentesque Malesuada
  //   example 1: base64_encode('Kevin van Zonneveld');
  //   returns 1: 'S2V2aW4gdmFuIFpvbm5ldmVsZA=='
  //   example 2: base64_encode('a');
  //   returns 2: 'YQ=='

  var b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
    ac = 0,
    enc = '',
    tmp_arr = [];

  if (!data) {
    return data;
  }

  do { // pack three octets into four hexets
    o1 = data.charCodeAt(i++);
    o2 = data.charCodeAt(i++);
    o3 = data.charCodeAt(i++);

    bits = o1 << 16 | o2 << 8 | o3;

    h1 = bits >> 18 & 0x3f;
    h2 = bits >> 12 & 0x3f;
    h3 = bits >> 6 & 0x3f;
    h4 = bits & 0x3f;

    // use hexets to index into b64, and append result to encoded string
    tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
  } while (i < data.length);

  enc = tmp_arr.join('');

  var r = data.length % 3;

  return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);
}

function base64_decode(s) {
    var e={},i,b=0,c,x,l=0,a,r='',w=String.fromCharCode,L=s.length;
    var A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for(i=0;i<64;i++){e[A.charAt(i)]=i;}
    for(x=0;x<L;x++){
        c=e[s.charAt(x)];b=(b<<6)+c;l+=6;
        while(l>=8){((a=(b>>>(l-=8))&0xff)||(x<(L-2)))&&(r+=w(a));}
    }
    return r;
}

function replaceAll(find, replace, str) {
  return str.replace(new RegExp(find, 'g'), replace);
}




window.onresize = updateFonts;
window.onload = updateFonts;
function updateFonts() {

  var viewPortWidth = window.innerWidth;

  if (viewPortWidth >= 600) {document.body.className= 'wide';}
  else if (viewPortWidth < 600) {document.body.className= 'thin';}
  // else if (viewPortWidth >= 1400) {$('body').addClass('wide').removeClass('extraWide, standard, narrow, extraNarrow')}
  // else if (viewPortWidth >= 1000) {$('body').addClass('standard').removeClass('extraWide, wide, narrow, extraNarrow')}
  // else if (viewPortWidth >= 700) {$('body').addClass('narrow').removeClass('extraWide, standard, wide, extraNarrow')}
  // else {$('body').addClass('extraNarrow').removeClass('extraWide, standard, wide, narrow')}



}


function showUsers(){
  document.getElementById('user-container').style.display="block";
}

function hideUsers(){
  document.getElementById('user-container').style.display="none";
}