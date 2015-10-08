nums = [1,2,3];
counts = [0,0,0];
range =20;
min=10;
delay = 100;

wonmsg= "<b style=\"color:green;\"> You Won!!! </b>";
lostmsg= "<b style=\"color:red;\"> Sorry, nothing for you! </b>";


play=false;

window.onload = function(){
	document.getElementById("button").onclick=start;
};



function showBlueButton(){
	document.getElementById('button').children[0].src="button2.jpg";
}

function showGreenButton(){
	document.getElementById('button').children[0].src="button1.jpg";
}


function start(){
	if(play)
		return;
	play =true;
	showBlueButton();
	initCounts();	
	createIntervals();
}





function createIntervals(){
	interval1 = setInterval(function() {
    	counts[0]--;
    	nums[0] = (nums[0]+1)%6;
    	showSymbols();
    	if(counts[0]==0)
    		window.clearInterval(interval1);    	

    	if(counts[2]==0&&counts[1]==0&&counts[0]==0)
    		end();
	}, delay);

	interval2 = setInterval(function() {		
    	counts[1]--;
    	nums[1] = (nums[1]+1)%6;
    	showSymbols();    	
    	if(counts[1]==0)
    		window.clearInterval(interval2);
    	if(counts[2]==0&&counts[1]==0&&counts[0]==0)
    		end();

	}, delay);

	interval3 = setInterval(function() {
		// console.log(nums);

    	counts[2]--;
    	nums[2] = (nums[2]+1)%6;
    	showSymbols();    
    	if(counts[2]==0)
    		window.clearInterval(interval3);	
    	if(counts[2]==0&&counts[1]==0&&counts[0]==0)
    		end();
	}, delay);
}

function initCounts(){
	counts[0] = min+Math.ceil(Math.random()*range);
	counts[1] = min+Math.ceil(Math.random()*range+range);
	counts[2] = min+Math.ceil(Math.random()*range+range*2);
}

function showSymbols(){
	document.getElementsByClassName('slot')[0].children[0].src="symbols"+(nums[0]+1)+".jpg";
	document.getElementsByClassName('slot')[1].children[0].src="symbols"+(nums[1]+1)+".jpg";
	document.getElementsByClassName('slot')[2].children[0].src="symbols"+(nums[2]+1)+".jpg";
}

function end(){	
	console.log(nums);
	showMsg();
}


function showMsg(){
	document.getElementById("msg").style.display ="block";
	document.getElementById("slotmachine-container").style.opacity="0.2";

	if(nums[0]==nums[1]&&nums[2]==nums[2]){
		document.getElementById('msg').children[0].innerHTML=wonmsg;
	}
	else{
		document.getElementById('msg').children[0].innerHTML=lostmsg;
	}

	document.getElementById("close").onclick=function(event){
		document.getElementById("msg").style.display="none";
		document.getElementById("slotmachine-container").style.opacity="1";
		showGreenButton();
		play=false;
	};
}

