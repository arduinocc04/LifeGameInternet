const le = 40, wi =20, pad = 20;
const sizes = Array.from({length: le}, (v, k) => (k * wi) + pad);
var mat = Array.from({length: le}, (v, k) => Array.from({length: le}, (v, k) => false));
const colors = ["#FF0000", "#00FF00", "#0000FF", "#000000"];
var current = 3;
var interval = null;
var frame = 0;
var maxCnt = 10;
var toNext = 300;
var cnt = 0;
var prevCellCnt = 0;
var prevNSameCnt = 0;
let startTime = 0;
var delayedTime = 0;
var image;
window.onload = function() {
	var ca = document.getElementById("generalCanvas");
	ca.height = sizes[le - 1] + wi + 1;
	ca.width = sizes[le -1] + wi + 1;
	let ctx = ca.getContext("2d");
	for(r of sizes){
		for(c of sizes){
			ctx.strokeRect(r,c,wi,wi);
		}
	}
	ca.onclick = (e) => {
		let re = ca.getBoundingClientRect();
		let x = e.clientX - re.left;
		let y =	e.clientY - re.top;
		fillRectangle(ctx, x, y);
		
	}
	name = prompt("닉네임을 입력하세요!");
	if(name == null || name == "" || name == "null") name = Math.random().toString(36).substr(2,9)
	var today = new Date();
	startTime = today.getTime();
	/*
	var raw = prompt("최대 세포개수를 입력하세요(자연수)");
	maxCnt = parseInt(raw);
	raw = prompt("한 프레임이 넘어갈때 몇 밀리초 기다리길 원하십니까?(1000밀리초 = 1초)");
	toNext = parseInt(raw);
	*/
	//document.getElementById("maxCnt").textContent = maxCnt;
	//document.getElementById("cnt").textContent = cnt;
	//document.getElementById("nColor").textContent = colors[current];
	clearCanvas();
}



function start(){
	image = document.getElementById("generalCanvas").toDataURL();
	if(maxCnt != cnt) {
		alert(maxCnt + "개를 채우세요!" + "현재 " + (maxCnt - cnt) + "개 남았습니다.");
		return;
	}
	var today = new Date();
	delayedTime = today.getTime() - startTime;
	if(!interval){
		interval = window.setInterval(update, toNext);
	}
	//document.getElementById("mode").textContent = "not stopped";
}

function stop(){
	if(interval){
		window.clearInterval(interval);
		interval = null;
	}
	//document.getElementById("mode").textContent = "stopped";
}

function update(){
	var mCellCnt = count();
	scan();
	reDraw();
	if (parseInt(document.getElementById("mCellCnt").value) < mCellCnt) document.getElementById("mCellCnt").value = mCellCnt;
	if(prevCellCnt == mCellCnt) prevNSameCnt++;
	if(prevNSameCnt>10) end();
	prevCellCnt = mCellCnt;
	if(mCellCnt == 0) end();
	//document.getElementById("frame").textContent = frame;
	frame++;
}

function end() {
	stop();
	var score = (5000 * mCellCnt * mCellCnt * Math.sqrt(frame))/Math.pow(delayedTime, Math.SQRT2);
	var data = new Object();
	data.name = name;
	data.mCellCnt = parseInt(document.getElementById("mCellCnt").value);
	data.frame = frame;
	data.delayedTime = delayedTime;
	data.score = score;
	data.image = image;
	var jsonData = JSON.stringify(data);
	var url = "/score";
	var request = new XMLHttpRequest();
	request.open("POST", url);
	request.setRequestHeader('Content-Type', 'application/json');
	request.send(jsonData)
	request.onload = function() {
		if(request.status == 200 || request.status == 201) window.location.href = "/scoreboard?name=" + name;;
	}
}

function setMax() {
	try{
		maxCnt = parseInt(document.getElementById("updateMax").value);

	}
	catch{
		maxCnt = 10;
	}
	document.getElementById("maxCnt").textContent = maxCnt;
}

function checkNears(targetX, targetY){
	let result = 0;
	targetX = parseInt(targetX);
	targetY = parseInt(targetY);
	let	stopX = targetX != mat.length - 1 ? targetX + 1 : targetX;
	let stopY = targetY != mat.length - 1 ? targetY + 1 : targetY;
	for(let i = targetX != 0 ? targetX - 1 : targetX; i <= stopX; i++){
		for(let j = targetY != 0 ? targetY - 1 : targetY; j <= stopY; j++){
			if(mat[i][j] && !(targetX == i && targetY == j)){
				result++;
			}
		}
	}
	return result;
}

function copyMat(){
	return Array.from({length: le}, (v, k) => Array.from({length: le}, (vv, kk) => mat[k][kk]))
}

function count() {
	var cnt = 0;
	for(r in mat) {
		for(c in mat[r]) {
			if(mat[r][c]) cnt++;
		}
	}
	return cnt;
}

function scan(){
	let current = 0;
	let tmp = copyMat();
	for(r in mat){
		for(c in mat[r]){
			current = checkNears(r, c);
			if(mat[r][c]){
				if(current < 2 || current > 3){
					tmp[r][c] = false;
				}
			}else{
				if(current == 3){
					tmp[r][c] = true;
				}
			}
		}
	}
	mat = tmp;
}

function set(a){
	if(a >= 0 && a <= colors.length){
		current = a;
	}else{
		throw new RangeError();
	}
	//document.getElementById("nColor").textContent = colors[current];
}

function fillRectangle(ctx, x, y){
	let rectX = adjustCoordinates(sqX = (~~((x - pad) / wi)));
	let rectY = adjustCoordinates(sqY = (~~((y - pad) / wi)));
	if(!mat[sqX][sqY]){
		if(cnt >= maxCnt) return;
		ctx.fillStyle = colors[current];
		cnt++;
	}else{
		ctx.fillStyle = "#FFFFFF";
		cnt--;
	}
	ctx.fillRect(rectX, rectY, wi, wi);
	ctx.strokeRect(rectX, rectY, wi, wi);
	mat[sqX][sqY] = !mat[sqX][sqY];
	//document.getElementById("cnt").textContent = cnt;
}

function adjustCoordinates(input){
	return input * wi + pad
}

function reDraw(){
	let ctx = this.document.getElementById("generalCanvas").getContext("2d");
	for(r in mat){
		for(c in mat[r]){
			if(mat[r][c]){
				ctx.fillStyle = "#000000";
			}else{
				ctx.fillStyle = "#FFFFFF";
			}
			ctx.fillRect(adjustCoordinates(r), adjustCoordinates(c), wi, wi);
			ctx.strokeRect(adjustCoordinates(r), adjustCoordinates(c), wi, wi);
		}
	}
}

function clearCanvas(){
	let ctx = this.document.getElementById("generalCanvas").getContext("2d");
	cnt = 0;
	ctx.fillStyle = "#FFFFFF";
	for(r in mat){
		for(c in mat[r]){
			if(mat[r][c]){	
				ctx.fillRect(adjustCoordinates(r), adjustCoordinates(c), wi, wi);
				ctx.strokeRect(adjustCoordinates(r), adjustCoordinates(c), wi, wi);
				mat[r][c] = false;
			}
		}
	}
	//document.getElementById("cnt").textContent = cnt;
	frame = 0;
	//document.getElementById("frame").textContent = frame;
	document.getElementById("mCellCnt").value = 0;
	var today = new Date();
	startTime = today.getTime();
	stop();
	//alert("cleared!");
}
