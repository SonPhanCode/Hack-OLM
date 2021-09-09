import pyautogui
import time
import stdiomask
import pyperclip
from selenium import webdriver
code_hack = r"""
(function(d){d.fn.ClassyLoader=function(a){a=d.extend({},{width:200,height:200,animate:!0,displayOnLoad:!0,percentage:100,speed:1,roundedLine:!1,showRemaining:!0,fontFamily:"Helvetica",fontSize:"50px",showText:!0,diameter:80,fontColor:"rgba(25, 25, 25, 0.6)",lineColor:"rgba(55, 55, 55, 1)",remainingLineColor:"rgba(55, 55, 55, 0.4)",lineWidth:5,start:"left"},a);var e=d(this);this.draw=function(b){"undefined"!==typeof b&&(a.percentage=b);var c=e[0].getContext("2d"),h=e.width()/2,d=e.height()/2,f=0, g=0;c.scale(1,1);c.lineWidth=a.lineWidth;c.strokeStyle=a.lineColour;setTimeout(function k(){var b=Math.PI/180*360/100*(f+1),b=b||Math.PI/180*360/100*(f+1);c.clearRect(0,0,e.width(),e.height());!0===a.showRemaining&&(c.beginPath(),c.strokeStyle=a.remainingLineColor,c.arc(h,d,a.diameter,0,360),c.stroke(),c.closePath());c.strokeStyle=a.lineColor;c.beginPath();c.lineCap=!0===a.roundedLine?"round":"butt";switch(a.start){case "top":g=1.5*Math.PI;break;case "bottom":g=.5*Math.PI;break;case "right":g=1*Math.PI; break;default:g=0}c.arc(h,d,a.diameter,g,b+g);c.stroke();c.closePath();!0===a.showText&&(c.fillStyle=a.fontColor,c.font=a.fontSize+" "+a.fontFamily,c.textAlign="center",c.textBaseline="middle",c.fillText(f+1+"%",h,d));f+=1;f<a.percentage&&setTimeout(k,a.speed)},a.speed)};this.setPercent=function(b){a.percentage=b;return this};this.getPercent=function(){return a.percentage};this.show=function(){var b=e[0].getContext("2d"),c=e.width()/2,d=e.height()/2;b.scale(1,1);b.lineWidth=a.lineWidth;b.strokeStyle= a.lineColour;b.clearRect(0,0,e.width(),e.height());b.strokeStyle=a.lineColor;b.beginPath();b.arc(c,d,a.diameter,0,Math.PI/180*(a.percentage/100)*360);b.stroke();b.closePath();!0===a.showText&&(b.fillStyle=a.fontColor,b.font=a.fontSize+" "+a.font,b.textAlign="center",b.textBaseline="middle",b.fillText(a.percentage+"%",c,d));!0===a.showRemaining&&(b.beginPath(),b.strokeStyle=a.remainingLineColor,b.arc(c,d,a.diameter,0,360),b.stroke(),b.closePath())};this.__constructor=function(){d(this).attr("width", a.width);d(this).attr("height",a.height);!0===a.displayOnLoad&&(!0===a.animate?this.draw():this.show());return this};return this.__constructor()}})(jQuery);

!function(w){

	function onDailyLimited()
	{
		$('#btn-done').remove();
		$("#count_prc").parent().addClass("alert-error");
		$("#std_btn").html('<p  style="font-size: 18px; line-height: 30px;">Bạn đã làm hết số câu hỏi miễn phí trong hôm nay, vui lòng quay lại thực hành vào ngày mai hoặc nâng cấp lên tài khoản VIP của OLM để tiếp tục thực hành <a class="btn btn-danger" href="/?l=payment.buy">Mua tài khoản VIP</a></p>');
	}
	
	function onGuestLimited()
	{
		$('#btn-done').remove();
		$("#count_prc").parent().addClass("alert-error");
		$("#std_btn").html('<p  style="font-size: 18px; line-height: 30px;">Để tiếp tục luyện tập, mời bạn đăng nhập <a class="btn btn-danger" href="/index.php?l=user.login">Đăng nhập</a></p>');		
	}

	function olm_set_item(key, val)
	{
		localStorage.setItem(key,val);
	}

	function olm_get_item(key, def)
	{
		var t = localStorage.getItem(key);
		return (t) ?  t : def;
	}

	function olm_clear_data(id_user)
	{
		var counting = parseInt( olm_get_item("stack.counting_" + id_user, 0) ); counting = counting  ? counting : 0;
		for(var i = 0; i< counting; i++)
		{		
			localStorage.removeItem("practice_data_" + id_user + "_" + i);
		}
		olm_set_item("stack.counting_" + id_user, 0 );
	}

    var isReportMode = false, qcode = "";
	var skillImage = function()
	{
		this.appendTo = function(id, repeat, attr)
		{
			if(!attr) attr = "";
			for(var i = 0 ;i < repeat; i++)
			{ 
				document.getElementById(id).innerHTML += "<img src='"+this.url+"' "+attr+" />"; 
			}
		}
	};

	var _text = ['Tuyệt vời !', 'Đúng rồi !', 'Xuất sắc !', 'Rất tốt !', 'Chính xác !', 'Yeah !!!','Giỏi quá !', 'Hay quá !','Khá lắm !'];
	var CONNECTION_ERROR = "Chúng tôi không kết nối được tới máy chủ OnlineMath vào lúc này, hãy kiểm tra kết nối Internet của bạn hoặc thử lại !";
	var CANNOT_LOAD_SCRIPT = "Có lỗi khi tải kỹ năng này. Hãy thử tải lại trang !"; // invalid token or time out
	//var _RENDERER = [];
	var _current_index = 0;
	var CF = function(){}
	var audioList = [];
	var current_q = -1;
	var previous_q = 0;
	var feedback_q = 0;
	var indexList = -1;
	var list_quiz = [];
	var matrix_q = [];
	var matrix_ans = []; //Ma trận đúng sai
	var matrix_result = []; //Ma trận kết quả
	var total_score = 0; 
	var paramsList = [];
	var resultList = [];
	var timeList = [];
	var quizList = [];
	var data_log = [];
	var total_time = 0;
	var times = 3;//Số câu hỏi cần trả lời để lưu
	var q_remain = 0; //Số câu còn lại để lưu
	var count_q = 0; //Đếm số câu luyện tập
	//var answered = 0;
	var total_q = 0;
	var set_lang = 'vi';
	var Lang_play = [];
	Lang_play["vi"] = {
		good : ['Tuyệt vời!', 'Đúng rồi!', 'Xuất sắc!', 'Rất tốt!', 'Chính xác!', 'Yeah!','Giỏi quá!', 'Hay quá!','Tốt lắm!'],
		cannot_load_script : "Có lỗi khi tải kỹ năng này. Hãy thử tải lại trang !",
		lesson_is_creating : "Bài học này đang được soạn nội dung",
		lesson_is_done: "Bạn đã hoàn thành bài học này",
		number_question: "Số câu hỏi",
		number_correct: "Số câu trả lời đúng",
		number_wrong: "Số câu sai",
		correct_rate: "Tỷ lệ đúng",
		replay: "Luyện tập lại!",
		history: "Lịch sử luyện tập",
		true_ans: "Đáp án đúng:",
		self_check: "Tự luận",
		continue_play: "Tiếp tục làm bài !",
		go_back: "Trở lại",
		report_err: "Báo lỗi",
		report: "Báo lỗi câu hỏi này và nhận thưởng VIP",
		summaries: "Lý thuyết",
		flashcard: "Flashcard",
		not_answer: "Chưa trả lời",
		correct: "Đúng",
		wrong: "Sai",
		completed: "Hoàn thành",
		your_play: "Câu hỏi và câu trả lời của bạn:",
		correct_ans: "Đáp án đúng",
		hint: "Ấn phím mũi tên trái / phải trên bàn phím để chuyển sang câu tiếp theo.",
		not_play: "Bạn chưa trả lời câu hỏi này, nếu bạn ấn nộp bài thì câu hỏi này sẽ được tính là bạn làm sai !",
		summit_quiz: "Nộp bài",
		delete_record: "Bạn có muốn xoá dữ liệu ở dạng bài này và thực hành lại?",
		deleted: "Đã xoá dữ liệu thực hành ở bài học này",
		error_database: "Lỗi cập nhật dữ liệu",
		error_connect_server: "Lỗi kết nối với máy chủ"
	};
	Lang_play["en"] = {
		good : ['Correct!','Fantastic!', 'Good work!', 'Well done!', 'Good job!', 'Great!', 'Wonderful!' ,'Superb!', 'Brilliant!', 'Excellent!', 'Awesome!', 'Great work!', 'Great job!', 'Nice work!', 'That’s right!', 'You got it!' ],
		cannot_Load_script : "Error when load this page. Please reload this page !",
		lesson_is_creating : "This lesson is being edited",
		lesson_is_done: "You have completed this lesson",
		number_question: "Number of questions",
		number_correct: "Number of correct answers",
		number_wrong: "Number of wrong answers",
		correct_rate: "Correct rate",
		replay: "Practice again!",
		history: "History of practice",
		true_ans: "Correct answer:",
		self_check: "Self check",
		continue_play: "Continue",
		go_back: "Go back",
		report_err: "Report",
		report: "Report this question and get VIP privileges",
		summaries: "Summary",
		flashcard: "Flashcard",	
		not_answer: "Unanswered",
		correct: "Correct",
		wrong: "Wrong",
		completed: "Completed",
		your_play: "Your question and answer:",
		correct_ans: "Correct answer",
		hint: "Press the left / right arrow keys on the keyboard to move on to the next question.",
		not_play: "You did not finish the question. Do you want to go back to the question?",
		summit_quiz: "Submit",
		delete_record: "Your practice in this lesson will be deleted if you press OK. Do you want to practice again?",
		deleted: "Your practice in this lesson was deleted.",
		error_database: "Error updating data",
		error_connect_server: "Error connecting to server"	
	};
	var p_lang = false;	
	CF.user = 
	{
		name: "Bạn",
		id: 0,
		image: "/images/avt/default/d0.png"
	}

	CF.createAudio = function()
	{
		var onReady = function()
		{
            for(var i = 0; i< audioList.length; i++){ soundManager.createSound(audioList[i]); }
		}
		if(soundManager.readyState!= 3){ soundManager.onready(function(){ onReady();}); return ""; }
		else{ onReady(); }
		return "";
	};

	CF.destroyAudio = function()
	{
		for(var i = 0; i< audioList.length; i++){ soundManager.destroySound(audioList[i].id); }	
	};
	CF.audioText = function(string)
	{
		var patt=/\(|\)|\+|\-|\*|\/|\.|,|\?|\'|\"|\?|\!|-|=|\>|\<|\[|\]|\s|:/g; // Remove: ( ) + - * / . , ? " ' ! - = > < [ ] :
		var url = CF.baseUrl() + "/skill/loadaudio.php?q=";
		var astring = string.split("_");
		var dstring = astring.join(" ").replace(/#/g,"");
		var l = [];
		for(var i = 0; i < astring.length; i++)
		{
			var s = astring[i];
			s = CF.viFilter(s).replace(patt,"");
			l.push(s);
		}
		var info  = l.join("+").toLowerCase();
		url +=  encodeURIComponent(info) + "&d="+CF._idQuestion;
		var info2 = l.join("_");
		audioList.push({id: info2, url: url});
		var text = "<h2 class='audiotext'> <span class='audiobtn' onclick='return soundManager.play(\""+info2+"\")'></span> <span class='audiocont'>"+dstring+"</span></h2>";
		return text;
	}
    CF.audioText2 = function(string)
    {
        var patt=/\(|\)|\+|\-|\*|\/|\.|,|\?|\'|\"|\?|\!|-|=|\>|\<|\[|\]|\s|:/g; // Remove: ( ) + - * / . , ? " ' ! - = > < [ ] :
        var url = CF.baseUrl() + "skill/loadaudio2.php?q=";
        var astring = string.split("_");
        var dstring = astring.join(" ").replace(/#/g,"");
        dstring = dstring.replace(/@/g,"");
        var l = [];
        for(var i = 0; i < astring.length; i++)
        {
            var s = astring[i];
            s = CF.viFilter(s).replace(patt,"");
            l.push(s);
        }
        var info  = l.join("+").toLowerCase();
        url +=  encodeURIComponent(info) + "&d="+CF._idQuestion;
        var info2 = l.join("_");
        audioList.push({id: info2, url: url});
        var text = "<h2 class='audiotext'> <span class='audiobtn' onclick='return soundManager.play(\""+info2+"\")'></span> <span class='audiocont'>"+dstring+"</span></h2>";
        return text;
    }
	CF.viFilter = function(str)
	{
		var from = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ";
		from += from.toUpperCase();
		var to = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd";
		to+= to.toUpperCase();
		for (var i = 0, l = from.length; i < l; i++) { str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i)); }
		return str;
	}

	CF.randNext = function(x,y)
	{
		var d = y -x;
		var res = Math.round(Math.random()*d);
		return parseInt(x + res);
	}

	CF.random = function()
    {
        return Math.random();
    }

	var timer = new Object;
	timer._time = 0;
	timer._time_count = false;
	timer._time_interval = false;
    var Results = [], Scores = [], Answered = [];
    var c_answered=0,c_true_ans=0;
    var $question = false, $questionStatic = false;
    function RandNext(x,y)
	{
	    var d = y -x;
	    var res = Math.round(Math.random()*d);
	    return parseInt(x + res);
	}
	function Alert(content, callback)
	{
		$("#std_btn").hide();
		$question.html("").hide();
		//var text = _text[RandNext(0,_text.length - 1)];
		var text = p_lang.good[RandNext(0, p_lang.good.length - 1)];
	    $("#good").html(text);
		$("#verygood").fadeIn(500).delay(800).fadeOut(800, function(){ $question.show(); $("#std_btn").show(); return callback ? callback.call() : false;});	
	}
	function OnDone()
	{

		$("#std_btn").hide();
		//console.log(paramsList);
		//console.log(resultList);
		var qcount = resultList.length, wrong_c = qcount - c_true_ans;
		if(qcount == 0) qcount = CF.count_problems, c_true_ans = CF.correct, wrong_c = qcount - c_true_ans;
		var pc = Math.round(c_true_ans * 100 / qcount);
		if(matrix_q.length == 0 && total_score == 0) $question.html("<h2>Bài học này đang được soạn nội dung!</h2>");
		else 
		{
			$question.html("<h2>"+Cf.data.say+" đã hoàn thành bài học này</h2><div class='static-overview'><p>Số câu hỏi: <strong>"+qcount+"</strong></p><p>Số câu trả lời đúng: <strong>"+c_true_ans+"</strong></p><p>Tỷ lệ đúng: <strong>"+pc+" %</strong></p><button class = 'btn btn-primary' onclick = 'CFrame.deleteRec();'>Luyện tập lại!</button><button class = 'btn btn-default' onclick = 'CFrame.loadHistory();' style = 'margin-left: 5px;'>Lịch sử luyện tập</button><a class = 'btn btn-default' href = '"+CF.data.next_lesson_url+"' style = 'margin-left: 5px;'>Bài học tiếp theo</a></div>");
			setTimeout(function() { 
				CF.soundComplete.play(); 
				$("#menu-lesson").show();
			}, 500);
		}
	}		
	function onWrongAnswer(position)
	{
		//$("#std_btn").hide();
		$("#btn-done").hide();
		$("#ignore").hide();
		$("#btn-action").css("display", "inline-block");

		//return reportQuestion(position);
		if( RunNow.isCode === undefined)
		{
			param = paramsList[indexList].qparams
			$question.append("<div id = 'u_correct_h'><h3 class = 'review'>"+p_lang.true_ans+"</h3><div id = 'u_correct'></div></div><div id = 'u_exp_h'><h3 class = 'review'>"+p_lang.hint+"</h3><div id = 'u_exp'></div></div>");
            RunNow.getContent(param , "u_correct");
            RunNow.getExp(param ,"u_exp");
		}
		else
		{
			$question.append("<div id = 'u_correct_h'>")
			if( [1,21].indexOf( RunNow.idq() ) === -1){
				$question.append("<h3 class = 'review'>"+p_lang.true_ans+"</h3><div id = 'u_correct'></div></div>");
				RunNow.makeCorrectAns($("#u_correct"));
			}
	        if( RunNow.exp != "" && RunNow.exp != undefined){
	        	$question.append("<div id = 'u_exp_h'><div id = 'u_exp'></div></div>");
	        	RunNow.getExp( $("#u_exp") );
	        	$("#btn-exp").show();
	        }
	        else $("#btn-exp").hide();
		}
		//$("#quizz").hide();
		//$("#btn-answer").addClass("btn-success");
		//$question.append("<a href='javascript:;' class='btn btn-primary resumeproc' onclick='return CFrame.next();'>Tiếp tục làm bài !</a>");
        //$question.append("<a onclick = 'CFrame.reportError();' title='Báo lỗi câu hỏi này và nhận thưởng VIP' class='btn btn-warning resumeproc'><b class='icon icon-ban-circle'></b> Báo lỗi</a>");
        $(".qholder input").attr("disabled","disabled");	
        $("#quizz .qselect").each( function(i,e){e.onclick = function(){} });			
	}
	CF.question = function(elm)
	{
		$(elm).parent().find("button").removeClass("btn-success");
		$(elm).addClass("btn-success");
		$("#quizz").show();
		$("#u_correct_h").hide();
		$("#u_exp_h").hide();

	}
	CF.answer = function(elm)
	{
		$(elm).parent().find("button").removeClass("btn-success");
		$(elm).addClass("btn-success");
		$("#quizz").hide();
		$("#u_correct_h").show();
		$("#u_exp_h").hide();

	}
	CF.exp = function(elm)
	{
		$(elm).parent().find("button").removeClass("btn-success");
		$(elm).addClass("btn-success");
		$("#quizz").hide();
		$("#u_correct_h").hide();
		$("#u_exp_h").show();

	}
	function reportQuestion(position, quiz){
		timer._time = timeList[position] - 1;
		feedback_q = quiz;
		current_q = previous_q;
		//$("#std_btn").hide();
		$("#btn-done").hide();
		$("#btn-action").css("display", "inline-block");
		$("#btn-action>button").hide();
    	var i = matrix_q[quiz];
    	var res = resultList[position];
    	var id_quiz = CFrame._list[i].id_script, param = paramsList[position].qparams, ans = paramsList[position].aparams;
    	if(quizList[position] > 0 ) id_quiz = quizList[position];
    	$question.html("<div id = 'u_result'></div>");
	    if(res == 2)
	    {
            $question.find("#u_result").html(" <span class = 'noans'> "+p_lang.not_answer+"</span>");
        }
	    else if(res == 1)
	    {
            $question.find("#u_result").html(" <span class = 'right'> "+p_lang.correct+"  </span>");
        }
        else
        {
            $question.find("#u_result").html(" <span class = 'wrong'> "+p_lang.wrong+"</span>");
        }
        if(CF.teacher) $question.append("<p style = 'color: #0044cc;'>ID: "+id_quiz +"</p>");
		if( CFrame._list[i].type==1)
		{
			$question.append("<h3 class = 'review'>"+p_lang.your_play+"</h3><div id = 'u_quiz'></div><h3 class = 'review'>Câu trả lời của "+(Cf.data.say == 'Bạn' ? 'bạn' : Cf.data.say)+":</h3><div id = 'u_ans'></div><h3 class = 'review'>"+p_lang.correct_ans+"</h3><div id = 'u_correct'></div><h3 class = 'review'>"+p_lang.hint+"</h3><div id = 'u_exp'></div>");
             _current_index = position;
			var scriptName = "script" + id_quiz;
           // _RENDERER[i] =  eval("new " + scriptName +";");           
            var quiz = eval("new " + scriptName +";"); 
            quiz.makeQuestion(param, "u_quiz");
           	quiz.getUA(param , ans , "u_ans");
           	quiz.getContent(param , "u_correct");
            quiz.getExp(param ,"u_exp");
            if(CF.teacher) $("#admin-edit").attr("href", "https://olm.vn/adm/?l=math.edittmpscript&id="+id_quiz);
		}
		else
		{
			//var tmp_elm = document.createElement("div"); 
			//tmp_elm.innerHTML = list_quiz['n'+id_quiz].content;
	        if(param == 0) param = undefined;
	        if(ans instanceof Array) ans = JSON.stringify(ans);
	        var runHistory = detectQuestion(list_quiz['n'+id_quiz].content, {
	            "id_quiz": id_quiz,
	            //"id_skill": object.id_skill,
	            "answer": ans,
	            //"time_spent": object.time_spent,
	            "result": res,
	            "params": param
	        }, { lang: set_lang, cdn: 'https://olm.vn/'});

	        $question.append("<h3 class = 'review'>Câu hỏi và câu trả lời của "+(Cf.data.say == 'Bạn' ? 'bạn' : Cf.data.say)+":</h3><div id = 'u_quiz'></div>")
	        runHistory.makeQuestionH($("#u_quiz")); 
	        if( [1,21].indexOf( runHistory.idq() ) === -1){
	        	$question.append("<h3 class = 'review'>"+p_lang.correct_ans+"</h3><div id = 'u_correct'></div>");
	        	runHistory.makeCorrectAns($("#u_correct"));
	    	}
	        if(runHistory.exp != "" && runHistory.exp != undefined){
	        	$question.append("<div id = 'u_exp'></div>");
	        	runHistory.getExp( $("#u_exp") );
	        }
			if(CF.teacher) $("#admin-edit").attr("href", "https://olm.vn/adm/?l=math.display.editquiz&id="+id_quiz);
		}
		CF.timeshow(timeList[position]);
		$question.append("<span style='font-size: 16px; color: #999999;'>Ấn phím mũi tên trái / phải trên bàn phím để chuyển sang câu tiếp theo.</span></br>");
		//if(total_score < 100) $question.append("<a href='javascript:;' class='btn btn-primary resumeproc' onclick='return CFrame.play();'>Tiếp tục làm bài !</a>");
       	//$question.append("<a onclick = 'CFrame.reportError("+i+");' title='Báo lỗi câu hỏi này và nhận thưởng VIP' class='btn btn-warning resumeproc'><b class='icon icon-ban-circle'></b> Báo lỗi</a>");
       	if(total_score < 100){
			$("#btn-action>.btn-primary").show();
       	}
        $(".qholder input").attr("disabled","disabled");
	}
    function checkQuestion(position)
    {
        var result = 0, correct = 0;

        //$("#btn-done").attr("disabled","disabled");
        //var i = position;
        var i = matrix_q[position];
		if(CFrame._list[i].type== 1)
		{
        	//_current_index = i;
        	result =  1;
        	Results[position] = result;
        	if(result == 1){ correct = 1 }
		}
		else
		{
		        result = 1;
		        if(result === 4) result = 1;
		        var saved = RunNow.getSaveData();
		        if(saved.answer === "") saved.answer = "[]";
			Results[position] = result;
			if(result === 1){ correct = 1 }
			paramsList[indexList] = {"qparams": saved.params, "aparams": saved.answer };
		}
		matrix_ans[position] = correct;
		resultList[indexList] = result;
		timeList[indexList] = timer._time;
		quizList[indexList] = current_id_quiz;
        return result;
    }

    function submitQuestion(position)
    {
    	console.log("submitQuestion", position);
    	var result = checkQuestion(position);
    	matrix_result[indexList] = result;
        if(result == 2)
        {
			$("#modal-content").html("<h4>Bạn chưa trả lời câu hỏi này, nếu bạn ấn nộp bài thì câu hỏi này sẽ được tính là bạn chưa làm !</h4> <button class='btn btn-danger' id='btn-continue' type='button'>Nộp bài !</button> <button id='btn-cancel' data-dismiss='modal' class='btn btn-primary' type='button'>Tiếp tục làm bài</button>");
            $("#form").modal("show");
            CFrame.id("btn-continue").onclick = function()
           	{
           		saveAnswer(position);
           		$("#modal-content").html("");
           		$('#form').modal("hide");
           		return onWrongAnswer(position);
            }
            $("#btn-cancel").click(function()
            {
 				//$("#btn-done").removeAttr("disabled");
 				$("#btn-done").off("click").on('click',function(){ submitQuestion(position); });
            });
        }
        else if(result == 1)
		{ 
			saveAnswer(position);
			CF.soundCorrect.play();
			return Alert("Bạn đã trả lời đúng !", nextQuestion); 	
		}
		else if(result == 3){
			return false;
		}
		else
		{  
			saveAnswer(position);
			CF.soundWrong.play();
			return onWrongAnswer(position);
		}
    }

	//var _s_data = [], QLABEL = ['A','B','C','D','E','F','G','H','I', 'K','L','M'];
	//var RunAll = []; var ind_check = 0;
	var RunNow = false;
	/*
	function checkQuiz(id_quiz)
	{
        var chk = RunNow.check($question);
        var saved = RunNow.getSaveData();
        if(saved.answer == "") saved.answer = "[]";
        return { "result": chk, "aparams": saved.answer , "qparams": saved.params };
	}
	*/
	function makeQuiz(id_quiz)
	{
		//var tmp_elm = document.createElement("div"); 
		//console.log(list_quiz['n'+id_quiz].content);
		//tmp_elm.innerHTML = list_quiz['n'+id_quiz].content;
		if(list_quiz['n'+id_quiz] === undefined){
			CFrame._list.splice(current_q, 1);
			matrix_q.splice(current_q, 1);
			matrix_ans.splice(current_q, 1);
			total_q -= 1;
			current_q -= 1;
			setTimeout(function() {
				return nextQuestion();			
			}, 100);
		}
       	RunNow = detectQuestion(list_quiz['n'+id_quiz].content, undefined, { lang: set_lang, cdn: 'https://olm.vn/'} );
        RunNow.makeQuestion($("#quizz"));
	}

    function _getQuestionParams(type,position)
    {
    	var params = [];
		if(type == "q"){ params.push(paramsList[position].qparams); }
		else{ params.push(paramsList[position].aparams); }
        return JSON.stringify(params);
    }

    function modalCreate(content, callback)
    {
        if(document.getElementById('olm_modal')) return;
        var div = document.createElement('div'); div.id='olm_modal';
        div.setAttribute('class','modal-bg');
        div.innerHTML = "<div class='modal-container'><div class='modal-inner'>"+content+"</div></div>";
        document.getElementById('qholder').appendChild(div);
        if(callback) callback.call();
    }

    //var _old_data;
   // var _data_question = [];
   	function saveAll()
   	{
        if(CF.user.id != 0)
        {
        	var data = new Object();
        	data.id_both_skill = CF.data.id;
    	    data.id_skill = CFrame.id_skill;
        	data.data_log = JSON.stringify(data_log);
			data.time_spent =  total_time;
			data.score = total_score;
		    data.answered = c_answered;
        	data.c_true = c_true_ans;
        	data.id_lop = CFrame.id_grade;
        	data.id_courseware = CF.data.id_courseware;
        	data.id_subject = CF.data.id_subject;
        	data.id_course = CF.data.id_course;
        	data.count = count_q;
		    $.ajax({
		    	url: "?g=teacherquestion.savenewbothrec",
		    	type: "POST",
		    	"data": data,
		    	success: function(res)
		    	{
		    		//console.log(res);
		    		if(res == 'ok')
		    		{
		    			//c_answered += 1;
		    			//createProgress(c_true_ans, CFrame._list.length);
		    			data_log = [];
		    			console.log('ok');
		    		}
		    		else{
		    		 	alert(res);
		    		 	window.location.href = '/dangnhap?return='+CF.data.lesson_url;
		    		}
		    	},
		    	error: function(){ console.log('nono'); }
		    });
    	} 
    	count_q = 0;  		
   	}
   	function remmainSave(remain)
   	{
   		$("#quiz_down").html("Còn "+remain+" câu để lưu ...");
   	}
   	function saveAnswer(position)
   	{
    	//$("#btn-done").attr("disabled","disabled");
    	//answered += 1;
    	var c = 0, _w = 0;
    	total_score = calMark();
    	if(matrix_ans[position] == 1){ c = 1; c_true_ans += 1; createProgress(); }else _w = 1;
    	//Add question done
		var cw = matrix_result[indexList] == 1 ? 'q-correct' : 'q-wrong';	
		if(matrix_result[indexList] == 2) cw = 'q-noans';
		$questionStatic.append("<span data-stt = '"+indexList+"' data-quiz='"+position+"' class='q-static "+cw+"'></span>");
		
		loadQuestionDone();
    	//Quá hạn làm bài
    	if(CF.time_expired === 1){
    		return false;
    	}    	
    	var data = new Object();
    	//data.id_both_skill = CF.data.id;
    	//data.id_skill = CFrame.id_skill;
    	total_time += timer._time;
        data.q_params = _getQuestionParams("q",indexList);
        data.a_params = _getQuestionParams("a",indexList);
        data.result = matrix_result[indexList];
        //data._token = window._token;
        data.correct = c;
        data.wrong = _w;
        data.a_index = position;
        data.time_spent = timer._time;
        data_log.push(data);
        c_answered += 1;
        q_remain = times - c_answered % (times + 1);
    	if( q_remain === 0 || total_score >= 100){
    		saveAll();
    		$("#quiz_down").html("Đã lưu kết quả ...");
    	}
    	else{
    		remmainSave(q_remain);
    	}
    	
    	if(!CFrame.vip)
		{
			var prcc = olm_get_item("prcc");
			var today = new Date(); today = today.getDate() + "_" + today.getMonth();
			if(prcc)
			{	
				prcc = prcc.split(":");
				if(today == prcc[0]){
					prcc = parseInt(prcc[1]) + 1;
				}
				else
				{
					prcc = 1;	
				}
			}
			else
			{
				prcc = 1;
			}
			olm_set_item("prcc", today + ":" + prcc);
			CFrame._qcount -= 1; CFrame._qcount = Math.max(0,CFrame._qcount);
			$("#count_prc").html(CFrame._qcount);
			if(CFrame._qcount <= 0)
			{
				onDailyLimited();
			}
		}
   	}
	function updateCoureware()
	{
		if(CF.data.id_courseware != 0){
			var data = {};
			data.id_exam = CFrame.id_skill;
		    //data.id_grade = CFrame.id_grade;
		    data.id_student = CF.data.id_student;
		    data.id_group = CF.data.id_group;
		    data.id_courseware = CF.data.id_courseware;
		    data.type_cw = 6;
		    data.type_cate = "id_category";
		    data.link_url = CF.data.link_url;
		    $.ajax({
		    	url: "/?g=teachercategory.updatecoureware",
		    	type: "POST",
		    	"data": data,
		    	success: function(res)
		    	{
		    		console.log(res);
		    	},
		    	error: function(){ console.log('nono'); }
		    }); 
		}
	}  
	/* 	
    function updateCoureware()
    {
    	if(CF.data.id_courseware != 0){
			var data = {};
	    	data.id_skill = CFrame.id_skill;
	        data.id_grade = CFrame.id_grade;
	        data.id_student = CF.data.id_student;
	        data.id_group = CF.data.id_group;
	        data.id_courseware = CF.data.id_courseware;
	        data.type_cw = 3;		
		    $.ajax({
		    	url: "?g=math.updatecoureware",
		    	type: "POST",
		    	"data": data,
		    	success: function(res)
		    	{
		    		console.log(res);
		    	},
		    	error: function(){ console.log('nono'); }
		    }); 
	    }
	    else updateCoureware2();           	
    }
    */
	function next()
	{
		timer._time += 1;
		var min = parseInt(timer._time/60);
		var sec = timer._time%60;
		var htm = ""; htm += min < 10 ? '0' + min : min;
		htm += " : "; htm += sec < 10 ? '0' + sec : sec;
		$('#time').html(htm);
	}

	CF.timecount = function()
	{
		if(!timer._time_count)
		{
			timer._time_interval = setInterval(next,1000);
			timer._time_count = true;
		}
	}
	CF.timeshow = function(sec){
		timer._time = sec - 1;
		next();
		CF.timestop();
	}
	CF.timestop = function()
	{
	    timer._time = 0;
	    clearInterval(timer._time_interval);
	    timer._time_count = false;
	}
	CF.saveQparams = function(params)
	{
        if(isReportMode&&!CFrame.data.isRetry)
        {
            if(window.console){console.log(CFrame._list[_current_index]);}
            return false;
        }
		if(!paramsList[_current_index])  paramsList[_current_index] = {qparams: params, aparams: ""}
		else paramsList[_current_index].qparams = params;
	}

	CF.saveAparams = function(params)
	{
		if(!paramsList[_current_index])  paramsList[_current_index] = {qparams: "", aparams: params}
		else paramsList[_current_index].aparams = params;
	}
	CF._list = [];
	CF.loadScript = function()
	{
		//PrePare _list
		for(var i = 0; i < CF._list.length; i++){
			if( CF._list[i] == 0) CF._list.splice(i, 1);
		}
		if(CF.data.id_subject == 2) set_lang = "en";
		p_lang = Lang_play[set_lang];
		$question = $("#question"); $questionStatic = $("#question-static");
		//var _url = CF.server + '?g=math.q_script';
		var _url = '?g=math.q_script';
        CF.data.script_list = "0";
        CF.data.qlib_list = "0";
        total_q = CF._list.length;
        //Khởi tạo thời gian đã thực hành
        total_time = parseInt(CF.total_time);
        //Khởi tạo tổng điểm đã thực hành
		total_score = CF.score;//calMark();
        for(var i = 0; i < total_q; i++){
        	if(CF._list[i].type == '1') 
        		CF.data.script_list += "," + CF._list[i].id_script; 
        	else CF.data.qlib_list += "," + CF._list[i].id_script; 
        }
		$.ajax({
			url: _url,
			data: {"id_skill": CFrame.id_skill, "script_list" : CF.data.script_list, "typecontent": CFrame.typecontent},
			cache: false,
			method:'GET',
			//dataType: 'json',
			success: function(data)
			{
				eval(data);
				CF.loadQuiz();
			},
			error: function(){ alert(CANNOT_LOAD_SCRIPT); }
		});

		//Init for couseware
		updateCoureware();
		//Sound

		CF.soundCorrect = sound("correct");
		CF.soundWrong = sound("wrong");
		CF.soundComplete = sound("complete");
		var prcc = olm_get_item("prcc");
		var today = new Date(); today = today.getDate() + "_" + today.getMonth();
		if(prcc)
		{
			prcc = prcc.split(":");
			if(today == prcc[0])
			{
				prcc = parseInt(prcc[1]);
			}
			else
			{
				prcc = 0;			
			}			
		}
		else
		{
			prcc = 0;
		}
		if(!CFrame.vip){CFrame._qcount -= prcc;} CFrame._qcount = Math.max(0,CFrame._qcount);
		$("#count_prc").html(CFrame._qcount);
		
		if(!CFrame.vip && CFrame._qcount <= 0)
		{
			onDailyLimited();
		}
		
		setTimeout(function() {
			$("#wrong_delete").show();
		}, 5000);
	}
	CF.loadQuiz = function()
	{
		//var _url = CF.server + '?g=math.q_quiz';
		var _url = '?g=math.q_quiz';
		$.ajax({
			url: _url,
			data: {"id_skill": CFrame.id_skill, "id_subject": CF.data.id_subject, "qlib_list" : CF.data.qlib_list},
			cache: false,
			method:'GET',
			dataType: 'json',
			success: function(data)
			{
				orgList(data);
			},
			error: function(e){ console.log(e);alert(CANNOT_LOAD_SCRIPT); }
		});
	}	
	function orgList(data){
		//console.log(data);
		//var flag = [] //List question is coded
		for(var i = 0; i < data.length; i++){
			var name = "n"+data[i].id;
			list_quiz[name] = data[i];
			//if(data[i].code == 1) flag.push(data[i].id);
		}
		//Xác định các câu hỏi được lập trình
		var tmp_matrix_q = [];
		//console.log(CF._list);
		for(var i = 0; i < CF._list.length ; i++){
			//console.log(list_quiz["n" + CF._list[i].id_script]);
			if(CF._list[i].type == '1' || ( list_quiz["n" + CF._list[i].id_script] && list_quiz["n" + CF._list[i].id_script].code == '1' ) ){
			 	CF._list[i].code = 1;
				tmp_matrix_q.push(i);
			}
			else CF._list[i].code = 0;
			matrix_q.push(i); //Đặt câu hỏi vào ma trận các câu hỏi
		}
		//Nếu lượng câu hỏi nhỏ hơn 10 thì mới lặp lại các câu hỏi
		//if( matrix_q.length <= 10 ) matrix_q = matrix_q.concat(tmp_matrix_q);
		//Khởi tạo ma trận kết quả
		//data_log = CF._record.slice();
		initMatrixAns(CF._record);		
	}
	function initMatrixAns(record){
		//console.log(record);
		var static = "";
		//Khởi tạo bảng kết quả luyện tập đã làm
		for(var i = 0; i < matrix_q.length; i++) matrix_ans[i] = 0;
		c_answered = 	record.length; //Số câu đã trả lời.
		for(var i = 0; i < c_answered; i++){
			//Init record for question answerd
			var rec = record[i];
			var QPARAMS = JSON.parse(rec.q_params) , APARAMS = JSON.parse(rec.a_params);
			current_q = parseInt(rec.a_index);
			matrix_ans[current_q] = parseInt(rec.correct);
			//matrix_result[current_q] = parseInt(rec.result);
			if( QPARAMS[0] === undefined ){
				paramsList[i] = {"qparams" : rec.q_params, "aparams": rec.a_params};
			}
			else{
				paramsList[i] = {"qparams" : QPARAMS[0], "aparams": APARAMS[0]};
			}
			//console.log( "PArams List", paramsList[i]);
			resultList[i] = parseInt(rec.result);
			timeList[i] = rec.time_spent;
			quizList[i] = rec.id_quiz;
			var cw = rec.result == '1' ? 'q-correct' : 'q-wrong';
			if(rec.result == '2') cw = 'q-noans';	
			static += "<span data-stt='"+i+"' data-quiz = '"+current_q+"' class='q-static "+cw+"'></span>";
			c_true_ans += parseInt(rec.correct); //Tính tổng số câu đúng
		}
		indexList = c_answered - 1;
		//Static question was done
		$questionStatic.html(static);
		/*
		q_remain = times - c_answered % (times + 1);
		if(q_remain == 0) q_remain = times + 1;
		remmainSave(q_remain);		
		*/
		//Khởi tiến trình luyện tập tiếp theo
		createProgress();
		loadQuestionDone();
		if( total_score  >= 100 ) return OnDone(); 
		nextQuestion(); //Chạy câu hỏi tiếp theo

	}
	//Tính điểm luyện tập
	function calMark(){
		var total = matrix_ans.length;
		if(total <= 5){
			var cr = 0;
			for(var i = 0; i < total; i++){
				cr += matrix_ans[i];
			}
			return Math.round( cr * 100 / total );
		}
		var total1 = Math.floor(total / 2), total2 = total1 + Math.floor(total / 4);
		var n1 = 0, n2 = 0, n3 = 0;
		for(var i = 0; i < total; i++)
			if(i < total1) n1 += matrix_ans[i];
			else if(i >= total1 && i < total2) n2 += matrix_ans[i];
			else n3 += matrix_ans[i];
		return Math.round( n1 * 60 / total1 + n2 * 24 / ( total2 - total1 ) + n3 * 16 / ( total - total2 ));
	}
	var current_id_quiz = 0;
	function loadQuestion(position)
	{
		count_q += 1;
		feedback_q = position;
		$("#btn-done").show();
		$("#btn-action>button").show();
		$("#btn-action").hide();
		$("#ignore").show();
		RunNow = false;
		indexList++;
		$("#std_btn").show();
		$( document ).off('keydown');
		//$("#btn-done").removeAttr("disabled");
		$question.html("<div id = 'quizz'></div>");
		$("#question-static>.q-static").removeClass("q-select");
		var i = matrix_q[position];
		console.log(position, matrix_q[position], CFrame._list[i]);
		current_id_quiz = CFrame._list[i].id_script;
		if(CFrame._list[i].type==1)
		{
			var scriptName = "script" + current_id_quiz;
			_current_index = indexList; //Tham số để lưu qparams
            RunNow  =  eval("new " + scriptName +";");
            RunNow.makeQuestion(false,"quizz");
            if(CF.teacher) $("#admin-edit").attr("href", "https://olm.vn/adm/?l=math.edittmpscript&id="+current_id_quiz);
		}
		else
		{
			makeQuiz(current_id_quiz);
			if(CF.teacher) $("#admin-edit").attr("href", "/?l=teachercourse.quiz&id_subject="+CF.data.id_subject+"&id="+current_id_quiz);
		}
		//Ipad key board
		if($(iPad.selector).length != 0)
        {
            iPad.defaultBehavior();
        }
        else iPad.remove(); 
 		$("#btn-done").off("click").on('click',function(){ submitQuestion(position); });
		if(CF.time_expired === 1){
			// $("#btn-done").attr("disabled","disabled");
			// $("#record-delete").remove();
			// $("#quizz input").attr("disabled","disabled");
			$("#quizz").append("<p style = 'font-size: 16px; color: #f22727;'>Bạn đã hết hạn làm bài này, nên kết quả luyện tập sẽ không được thay đổi và lưu lại. Hãy liên hệ với giáo viên phụ trách để gia hạn thời gian làm bài!</p>");
		}
		else{
			CF.timestop();
			CF.timecount();
		}
		disableAll();
	}
	function loadQuestionDone(){
		if($("#question-static>.q-static").length > 0){
			$("#question-static>.q-static").on("click", function(){
				$("#question-static>.q-static").removeClass("q-select");
				handleKeyReport(this);
			});
			$("#record-delete").show();
		}
	}
	function createProgress()
	{
		if(total_score == 0) total_score = CF.score;
        var mark = total_score;	
     	if(mark > 0){
	     	var html = '<h4>'+p_lang.completed+' <span>'+mark+'%</span></h4><canvas class="loader"></canvas>';
	    	$('#score-static').html(html);
	    	var loader = $('.loader').ClassyLoader({
			    animate: true,
			    percentage: mark,
			    speed: 1,
				width: 160, height: 160,
				diameter: 70,
				fontSize: "40px",
				fontFamily: "Tahoma",
				fontColor: 'rgba(0, 194, 52, 1)',
				lineColor: 'rgb(46, 194, 0)',
				remainingLineColor: 'rgba(46, 194, 0, 0.2)',
				lineWidth: 10
			});
			$("#record-delete").show();
	    }
		if(mark >= 100)
		{
			$('#contest-result').show();
		}
	}
	var isFullScreen = false;	
	function openFullscreen(elem) {
		$(elem).addClass("fullscreen");
	  isFullScreen = true;
	  if (elem.requestFullscreen) {
	    elem.requestFullscreen();
	  } else if (elem.mozRequestFullScreen) { /* Firefox */
	    elem.mozRequestFullScreen();
	  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
	    elem.webkitRequestFullscreen();
	  } else if (elem.msRequestFullscreen) { /* IE/Edge */
	    elem.msRequestFullscreen();
	  }
	}
	function closeFullscreen(elem) {
		$(elem).removeClass("fullscreen");
	  isFullScreen = false;
	  if (document.exitFullscreen) {
	    document.exitFullscreen();
	  } else if (document.mozCancelFullScreen) { /* Firefox */
	    document.mozCancelFullScreen();
	  } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
	    document.webkitExitFullscreen();
	  } else if (document.msExitFullscreen) { /* IE/Edge */
	    document.msExitFullscreen();
	  }
	}
	var fullScreenEvent = false;
	CF.fullscreen = function()
	{
		var elm = document.getElementById("qholder");
		if(window.innerHeight == screen.height){ 
			closeFullscreen(elm); 
		}
		else{ 
			openFullscreen(elm); 
		}
		if(!fullScreenEvent)
		document.addEventListener("fullscreenchange", function() {
			fullScreenEvent = true;
			if( $("#fullscreen-static").html() != "" ){ 
				$("#all-static").html($("#fullscreen-static").html()).show();
				$("#fullscreen-static").html("").hide();
			}
			else{ 
				$("#fullscreen-static").html($("#all-static").html()).show();
				$("#all-static").html("").hide();
			}
			createProgress();
			loadQuestionDone();			
		});
	}
	CF.deleteRec = function()
	{
		//Xử lý quá hạn làm bài
		if(CF.time_expired === 1){
			if(confirm(p_lang.delete_record))
			{
				for(var i = 0; i < matrix_q.length; i++) matrix_ans[i] = 0;
				total_score = 0;
				indexList = -1;
				resultList = [];
				timeList = [];
				quizList = [];
				current_q = 0;
				$("#score-static").html("");
				$("#question-static").html("");
				return loadQuestion(current_q);
			}
		}
		var id = CFrame.data.id;
		if(confirm(p_lang.delete_record))
		{
			$.ajax({
				url: "?g=teacherquestion.deletebothrec",
				type: 'POST',
				data: {id_both_skill: id, id_subject: CF.data.id_subject, id_skill : CFrame.id_skill},
				success: function(res)
				{
					//console.log(res);
					if(res == 'ok') location.reload();
					else alert(p_lang.error_database);
				},
				error: function() { alert(p_lang.error_connect_server); }
			});
		}
	}
	var repeat = 0; // Đếm số lần lặp
	var loop_q = false; //Lặp lại câu hỏi
	function nextQuestion(){
		//console.log(current_q);
		//console.log(CFrame.data.isG);
		if(current_q == 2 && CFrame.data.isG){ onGuestLimited(); }
		if(matrix_q.length == 0){ loop_q = false; return OnDone(); }
		if(!loop_q) previous_q = current_q;
		current_q++;
		if(current_q >= matrix_ans.length){ loop_q = true;  current_q = -1; nextQuestion();}
		else if( repeat >= matrix_ans.length || total_score >= 100 ){ 
			//updateCoureware();
			//loop_q = false;
			//saveAll();
			//return OnDone();
			location.reload(); 
		}
		else if( matrix_ans[current_q] == 1 ){ loop_q = true; repeat++;  nextQuestion(); }
		else{
			loop_q = false;
			repeat = 0;	
			loadQuestion(current_q);
		}
	}
	//Âm thanh đúng / sai
	function sound(status){
		var audio = new Audio(CF.server + 'modules/math/js/sound/'+status+'.mp3');
		audio.volume = 0.2;
		return audio;
	}	
    function disableAll(){
        document.addEventListener('contextmenu', event => event.preventDefault());
        document.onkeypress = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
        return false;
        }
        }
        document.onmousedown = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
        return false;
        }
        }
        document.onkeydown = function (event) {
        event = (event || window.event);
        if (event.keyCode == 123) {
        return false;
        }
        }
        jQuery(document).ready(function($){
        $(document).keydown(function(event) {
        var pressedKey = String.fromCharCode(event.keyCode).toLowerCase();

        if (event.ctrlKey && (pressedKey == "f" || pressedKey == "c" || pressedKey == "u")) {
        //alert('Sorry, This Functionality Has Been Disabled!');
        //disable key press porcessing
        return false;
        }
        });
        });    
    } 	
	CF.next = function()
	{
		nextQuestion();
	}
	CF.play = function()
	{
		loadQuestion(current_q);
	}
	CF.ignore = function(){
		submitQuestion(current_q)
   		//saveQuestion(current_q);
   		//return onWrongAnswer(current_q);		
	}
	CF.baseSiteUrl = function(){ return CF.server;}

	CF.getScore = function(){ return 100;}

	CF.closeModal = function(){ $("#olm_modal").remove(); }
	
	CF.error = function(e){ $("#error_panel").html("<p class='alert alert-error'> <button type='button' class='close' data-dismiss='alert'>&times;</button>"+e+"</p>");}

	CF.openNotice = function()
	{
		if(document.getElementById('olm_modal')) return;
		var div = document.createElement('div'); div.id='olm_modal';
		div.setAttribute('class','modal-bg');
		var content = "<h1>Bạn còn chưa trả lời câu hỏi !</h1><p>Nếu thấy quá khó, hãy bỏ qua và làm câu tiếp theo.</p><button class='btn btn-primary' onclick='_OLM_.closeModal();'>Đóng lại và tiếp tục</button> <button onclick='_OLM_.ignore();'class='btn btn-danger'>Bỏ qua câu này</button>";
		div.innerHTML = "<div class='modal-container'><div class='modal-inner'>"+content+"</div></div>";
		document.getElementById("qholder").appendChild(div);
	}

	CF.images = [
		{id:'gl1', name:'bộ chìa khóa', img:'bochiakhoa.png'},
		{id:'gl2', name:'bóng đèn', img:'bongden.png'},
		{id:'gl3', name:'bông hoa', img: 'bonghoa.png'},
		{id:'gl4', name:'quả bóng rổ', img:'bongro.png'},
		{id:'gl5', name:'bút lông', img:'butmau.png' },
		{id:'gl6', name:'cái chuông', img:'caichuong.png'},
		{id:'gl7', name:'con chim cánh cụt', img:'chimcanhcut.png'},
		{id:'gl8', name:'con cá', img:'conca.png'},
		{id:'gl9', name:'quả dâu', img: 'dau.png'},
		{id:'gl10', name:'quả dứa', img:'dua.png'},
		{id:'gl11', name:'chiếc kính lúp', img:'kinhlup.png'},
		{id:'gl12', name:'quả lê', img:'le.png'},
		{id:'gl13', name:'bẹ chuối', img:'naichuoi.png'},
		{id:'gl14', name:'ngôi nhà', img:'ngoinha.png'},
		{id:'gl15', name:'ngôi sao', img:'ngoisao.png'},
		{id:'gl16', name:'quả bóng', img:'quabong.png'},
		{id:'gl17', name:'quả bong bay', img:'quabongbay.png'},
		{id:'gl18', name:'quả cam', img:'quacam.png'},
		{id:'gl19', name:'quả đào', img:'quadao.png'},
		{id:'gl20', name:'cuốn sách', img:'sach.png'},
		{id:'gl21', name:'quả táo', img:'tao.png'},
		{id:'gl22', name:'cục tẩy', img:'taychi.png'}
	];
	
	CF.getImage = function(index)
	{
		var img = CF.images[index]; var image = new skillImage;
		image.id = img.id; image.name = img.name; image.url = CFrame.server + 'skill/images/'+img.img; image.html = "<img src='"+image.url+"' />";
		return image;
	}
	
	CF.randImage = function()
	{
		var length = this.images.length;
		var index = this.randNext(0, length-1);
		return this.getImage(index);
	}
	
	CF.getImageById = function(id)
	{
		var index = parseInt(id.substr(2,id.length));
		return this.getImage(index - 1);
	}
	
	CF.id = function(id){return document.getElementById(id);}
	
	CF.randList = function(list)
	{
		list1 = [];
		for(var i = 0; i < list.length;  i++) list1.push(list[i]);
		var result = [];
		le = list.length;
		while(le > 0)
		{
			var rd = CFrame.randNext(0,le - 1);
			var tmp = list1.splice(rd,1)
			result.push(tmp[0]);
			le--;
		}
		return result;
	}
	
	CF.jsonEncode = function(o){ return JSON.stringify(o); }

	CF.randNext = function(x,y)
	{
		var d = y -x;
		var res = Math.round(Math.random()*d);
		return parseInt(x + res);
	}

	CF.setExp = function(expc){ document.getElementById("contest-view").innerHTML = expc; }

	CF.addExp = function(expc){ document.getElementById("contest-view").innerHTML += expc; }

	CF.baseUrl = CF.baseSiteUrl;

	var CSS = [];

	CF.addStyleSheet = function(css)
	{
		head = document.getElementsByTagName('head')[0], 
		style = document.createElement('style'); 
		style.type = 'text/css'; 
		if(style.styleSheet){ style.styleSheet.cssText = css; }
		else{ style.appendChild(document.createTextNode(css)); }
		head.appendChild(style);
	}
	CF.loadHistory = function(){
		handleKeyReport();
	}
	function handleKeyReport(elm){
		var stat = $("#question-static>.q-static");
		var stt = 0, max = stat.length;
		if(elm == undefined) elm = stat[0];

        var q_stt = $(elm).data("stt");
        var q_quiz = $(elm).data("quiz");
        reportQuestion(q_stt, q_quiz);
        $(elm).addClass("q-select");
		//document.onkeydown = checkKeycode;
		$( document ).keydown(function(event) {
			$(".q-static").removeClass("q-select");
			var keyDownEvent = event || window.event,
	        keycode = (keyDownEvent.which) ? keyDownEvent.which : keyDownEvent.keyCode;			
	        if(keycode == 39){
	        	stt += 1;
	        }else if(keycode == 37){
	        	stt -= 1;
	        }
	        if(stt < 0) stt = max - 1;
	        if(stt >= max) stt = 0;
	        elm = stat[stt];
	        q_pos = $(elm).data("stt");
	        q_stt = $(elm).data("quiz");
	        $(elm).addClass("q-select");
	        reportQuestion(q_pos, q_stt);
		});		
	}
    CF.reportError = function()
    {
        if(document.getElementById('olm_modal')) return;
        var div = document.createElement('div'); div.id='olm_modal';
        div.setAttribute('class','modal-bg fade in'); //div.onclick = CFrame.closeModal;
        var modal_style ="style='width: 620px; padding: 5px 8px; background: #ffffff;opacity: 1; box-shadow: 0px 1px 10px #000; margin: 2.5% auto;'";
        var content = "<span class='close' onclick='CFrame.closeModal();'>&times;</span><h2 style='text-align: center;'>Báo lỗi câu hỏi</h2>";
        content += "<p>Bạn đã gặp lỗi gì ở câu hỏi này, hãy mô tả vào ô bên dưới. Với mỗi lỗi thông báo đúng, OLM sẽ thưởng cho bạn 10 ngày VIP!</p>";
        content += " <textarea class='form-control' rows='5' id='reportContent' placeholder = 'Hãy mô tả vài dòng về lỗi của bài toán này.' style = 'width: 97%;'></textarea>";
        var modal = "<div id='olm-modal-content' "+modal_style+"><div style='overflow: hidden; margin: 10px;' class='olm-question-list scroll'>"+content+"<p style='text-align: center;'><br /><button id = 'give-feedback' class='btn btn-primary' style = 'margin-right: 10px;'>Gửi báo lỗi</button><button onclick='CFrame.closeModal();' class='btn btn-danger'>Hủy</button></p><br class='clear'/></div></div>";
        div.innerHTML = modal;
        document.getElementById("qholder").appendChild(div); $(div).addClass("hidden-phone hidden-tablet");
        var iq = matrix_q[feedback_q];
		var quiz = CFrame._list[iq];

        $("#give-feedback").on("click", function(){
            var ct = $("#reportContent").val();
            if(ct === ""){alert("Bạn phải mô tả về lỗi của bài toán này."); return;}
            var _url = '?g=content.feedback';
            $.ajax({
                url: _url,
                type: "POST",
                data: {
                    id_question : quiz.id_script,
                    skill: CFrame.id_skill,
                    content : ct,
                    subject: CF.data.id_subject,
                    id_course: CF.data.id_course,
                    type : quiz.type
                },
                success: function(string){
                   // console.log(string);
                    if(string == "OK") { alert("Cảm ơn bạn đã báo lỗi, OLM sẽ xem xét phản hồi này của bạn!"); CFrame.closeModal();}
                    else if(string == "SORT") alert("Bạn vui lòng mô tả lỗi cụ thể hơn, cảm ơn bạn!");
                    else alert("Đã xảy ra lỗi, hãy gửi lại!");
                },
                error: function(){
                    alert("Lỗi kết nối đến máy chủ OLM, hãy thử lại!");
                }
            });
        });
    }
    CF.guide = function(iq)
    {
        if(document.getElementById('olm_modal')) return;
        var div = document.createElement('div'); div.id='olm_modal';
        div.setAttribute('class','modal-bg fade in'); //div.onclick = CFrame.closeModal;
        var modal_style ="style='width: 910px; padding: 5px 8px; background: #ffffff;opacity: 1; box-shadow: 0px 1px 10px #000; margin: 2.5% auto;'";
        var content = "<div id = 'modal_conent'><span class='close' onclick='CFrame.closeModal();'>&times;</span><h2 style='text-align: center;'>Hướng dẫn cách làm bài</h2>";
        content += "<p><iframe width='900' height='506' src='https://www.youtube.com/embed/dMcKuQY2C8o?autoplay=1' frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></p></div>";
        var modal = "<div id='olm-modal-content' "+modal_style+"><div style='overflow: hidden; margin: 10px;' class='olm-question-list scroll'>"+content+"<p style='text-align: center;'><br /><button onclick='CFrame.closeModal();' class='btn btn-primary'>Tôi đã hiểu</button>&nbsp;<button onclick='CFrame.listRestore();' class='btn btn-default'>Khôi phục điểm</button></p><br class='clear'/></div></div>";
        div.innerHTML = modal;
        document.getElementById("qholder").appendChild(div); $(div).addClass("hidden-phone hidden-tablet");
    }
    CF.listRestore = function()
    {
    	$("#modal_conent").html("<h2>Khôi phục điểm</h2><div id = 'listscore'></div>");
        var _url =  '?g=math.recdeleted';
        $.ajax({
            url: _url,
            type: "POST",
            data: {
                id_skill : CF.id_skill
            },
            success: function(string){
            	var data = JSON.parse(string);
            	if(data.length == 0){
            		alert("Không có dữ liệu khôi phục");
            		$("#listscore").html("Không có dữ liệu khôi phục điểm");
            	}
            	else{
            		var html = "<table class = 'table table-striped'><thead><tr><th>Ngày xóa</th><th>Đúng</th><th>Sai</th><th>Hoàn thành</th><th>Khôi phục</th></tr></thead>";
            		html += "<tbody>";
            		for(var i = 0; i < data.length; i++)
            			html += "<tr><td>"+data[i].created_date+"</td><td>"+data[i].correct+"</td><td>"+data[i].missed+"</td><td>"+data[i].score+"</td><td><button data-id = '"+data[i]._id+"' class = 'btn btn-default' onclick = 'CFrame.restoreScore(this)'>Khôi phục</button></td></tr>";
            		html += "</tbody></table>";
            		$("#listscore").html(html);
            	}
            },
            error: function(){
                alert("Lỗi kết nối đến máy chủ OLM, hãy thử lại!");
            }
        });		
    } 
    CF.restoreScore = function(elm)
    {
    	var id = $(elm).data('id');
        var _url = '?g=math.restorescore';
        $.ajax({
            url: _url,
            type: "POST",
            data: {
                id : id
            },
            success: function(string){
            	var data = JSON.parse(string);
            	if(data.status == 1){
            		alert("Đã khôi phục điểm");
            	}
            	else alert("Lỗi: " + data.message);
            },
            error: function(){
                alert("Lỗi kết nối đến máy chủ OLM, hãy thử lại!");
            }
        });	    	
    }   	
	CF.rN = CF.randNext;
	CF.rL = CF.randList;
	CF.rI = CF.randImage;

	window.CFrame = window.Cf = window._OLM_ = CF;
}(window);
(function(){
    window.iPad = function(){};
    iPad.keys = [0,1,2,3,4,5,6,7,8,9,'+','-','x',':','.',',',';','>','<','='];
    iPad.html  = "";
    iPad.selector = ".question input[type='text']";
    iPad.current = null;
    iPad.hidden = false;
    iPad.render = function(){
        iPad.html = "<div id='olm_key_pad'>";
        for(var i = 0; i < iPad.keys.length;i++)
        {
            iPad.html += "<button class='btn btn-small key-btn keypad'>"+iPad.keys[i]+"</button>";
        }
        iPad.html += "<button onclick='return iPad.backSpace();' class='btn keypad btn-small' style='padding: 0px 5px;'><b class='backspace'></b></button></div>";
    }

    iPad.keyPad = function(elm){
        $('#olm_keypad').remove();
        iPad.render(); elm.innerHTML = iPad.html;
        $('.key-btn').each(function(index, element) {
            element.onclick = function(){
                iPad.current.value +=$(element).text();
                iPad.sizeX();
            }
        });
    }

    iPad.sizeX = function(){
		var size = iPad.current.value.length * 15;
		if(size > 20) $(iPad.current).css("width", size);
		else $(iPad.current).css("width", 20);    	
    }

    iPad.dropTo = function(selector){
        iPad.selector = selector;
        $(selector).focus(function(){
            iPad.current = this;
        }).get(0).focus();
        iPad.current = $(selector).get(0);
    }

    iPad.show = function(){
        if($(iPad.selector).length != 0){
            iPad.keyPad(document.getElementById('ipad_container'));
            iPad.dropTo(iPad.selector);
        }
    }

    iPad.backSpace = function(){
        var val = iPad.current.value;
        val = val.substring(0,val.length-1);
        iPad.current.value = val;
        iPad.sizeX();
    }

    iPad.toggle = function(){
        if(iPad.hidden){
            iPad.show();
            iPad.hidden = false;
        }else{
            iPad.remove();
            iPad.hidden = true;
        }
    }

    iPad.remove = function(){
        $("#olm_key_pad").remove();
    }

    iPad.defaultBehavior = function(f){
        if(iPad.hidden){
            return;
        }
        iPad.show();
    }

    return false;
})();
"""
acc = input("Tài Khoản: ")
pwd = stdiomask.getpass("Mật Khẩu: ", mask="♠")
bai_tap = input("Nhập Link Bài Tập: ")
driver1 = webdriver.Chrome(executable_path="chromedriver.exe")
driver1.get("https://olm.vn/dangnhap")
tai_khoan = driver1.find_element_by_css_selector('#username_login_2')
tai_khoan.send_keys(acc)
mat_khau = driver1.find_element_by_css_selector('#password')
mat_khau.click()
mat_khau.send_keys(pwd)
time.sleep(1)
login = driver1.find_element_by_css_selector('#login-submit_2')
login.click()
time.sleep(1)
driver1.get(bai_tap)
pyautogui.hotkey("ctrl","shift","i")
time.sleep(2)
pyautogui.click(631,146)
time.sleep(1)
pyautogui.click(425,338)
time.sleep(1)
pyautogui.click(436,418)
time.sleep(1)
pyautogui.click(522,440)
time.sleep(1)
pyautogui.hotkey("ctrl","f")
pyautogui.typewrite("Runnow.check")
pyautogui.press("enter")
time.sleep(1)
pyautogui.click(798,459)
pyperclip.copy(code_hack)
pyautogui.hotkey("ctrl","a")
time.sleep(1)
pyautogui.hotkey("ctrl","v")
time.sleep(1)
pyautogui.hotkey("ctrl","s")
