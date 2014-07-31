   function sAlert(strTitle,strContent){
    var msgw,msgh,bordercolor;
    msgw=400;//提示窗口的宽度
    msgh=100;//提示窗口的高度
    titleheight=25 //提示窗口标题高度
    bordercolor="#051405";//提示窗口的边框颜色
    titlecolor="#7BBFEA";//提示窗口的标题颜色
    var sWidth,sHeight;
    sWidth=0;
    sHeight=0;
    var bgObj=document.createElement("div");
    bgObj.setAttribute('id','bgDiv');
    bgObj.style.position="absolute";
    bgObj.style.top="0";
    bgObj.style.background="#777";
    bgObj.style.opacity="0.6";
    bgObj.style.left="0";
    bgObj.style.width=sWidth + "px";
    bgObj.style.height=sHeight + "px";
    bgObj.style.zIndex = "10000";
    document.body.appendChild(bgObj);
    var msgObj=document.createElement("div")
    msgObj.setAttribute("id","msgDiv");
    msgObj.setAttribute("align","center");
    msgObj.style.background="#FFF1B5";
    msgObj.style.border="1px solid " + bordercolor;
    msgObj.style.position = "absolute";
    msgObj.style.left = "50%";
    msgObj.style.top = "50%";
    msgObj.style.font="24px Verdana, Geneva, Arial, Helvetica, sans-serif";
    msgObj.style.marginLeft = "-225px" ;
    msgObj.style.marginTop = -75+document.documentElement.scrollTop+"px";
    msgObj.style.width = msgw + "px";
    msgObj.style.height =msgh + "px";
    msgObj.style.textAlign = "center";
    msgObj.style.lineHeight ="25px";
    msgObj.style.zIndex = "10001";
    var title=document.createElement("h4");
    title.setAttribute("id","msgTitle");
    title.setAttribute("align","right");
    title.style.margin="0";
    title.style.padding="3px";
    title.style.background=bordercolor;
    title.style.opacity="0.75";
    title.style.border="1px solid " + bordercolor;
    title.style.height="20px";
    title.style.font="20px Verdana, Geneva, Arial, Helvetica, sans-serif";
    title.style.color="#000000";
    title.style.cursor="pointer";
    title.title = "点击关闭";
    title.innerHTML="<table border='0' width='100%'><tr><td align='left'><font color='#FFFFFF'><b>"+ strTitle +"</b></font></td><td align='right' ><font color='#FFFFFF'>关闭</font></td></tr></table></div>";
    title.onclick=function(){
    document.body.removeChild(bgObj);
    document.getElementById("msgDiv").removeChild(title);
    document.body.removeChild(msgObj);
    }
    document.body.appendChild(msgObj);
    document.getElementById("msgDiv").appendChild(title);
    var txt=document.createElement("p");
    txt.style.margin="1em 0"
    txt.setAttribute("id","msgTxt");
    txt.innerHTML=strContent;
    document.getElementById("msgDiv").appendChild(txt);
    }