const USER_GROUP = 0; 
const ASSIGNED = 1; 
const TICKET_INDEX = 2; 
const USER_INDEX = 3; 
const MIN_COMMENT_INDEX = 4; 


function getTicketInfo(ticket){
  const priority = {
    E: 'Emergency',
    U: 'Urgent',
    R: 'Routine'
  };

  const userGroup = {
    U: 'User',
    T: 'Tech'
  };

  let allTickets = "alltickets";
  let token = getCookie("csrftoken");

  $.ajax(
    {
        headers: { "X-CSRFToken": token },
        type:"POST",
        url: "/getticket/",
        data:{
                 "ticketNum": ticket,
        },
        success: function( response ) 
        {
          let ticketTable = document.getElementById("ticketDiv");
          let jsonReturn = JSON.parse(response)
          ticketTable.innerHTML = "";
          var commentCount = 0;
          var techAssigned = false;
          const currentUserGroup = jsonReturn[USER_GROUP] //grabs fist object from json which is current user's group 
          const isCurrentUserAssigned = jsonReturn[ASSIGNED] 
          const userInfo = jsonReturn[USER_INDEX];
          /*
          Since we are only passing 1 ticket with the possibily of multiple users and comments,
          we know the next object in jsonReturn will be the ticket
          */
          const ticketInfo = jsonReturn[TICKET_INDEX];
          ticketTable.innerHTML += "<p id='title'><strong>" + ticketInfo.title + "</strong></p>";
		  
          if (ticketInfo.is_assigned){
              assigned = "True";
              mark = "&#x2713;"
              techAssigned = true;
            }else{
              assigned = "False"
              mark = "&#x2715;"
            }	
          const ticketStatus = ticketInfo.status == "O" ? "Open" : "Close";

          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Ticket Number: </strong> " + ticketInfo.ticketNum + "</pre>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Status:              </strong> " + ticketStatus + "</pre>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Assigned:          </strong> <b class='assigned"+assigned+"'>" + mark +"</b></pre>";		  
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Priority:            </strong> " + priority[ticketInfo.priority] +"</pre><br>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Date Created:   </strong> " + (ticketInfo.date_created ? new Date(ticketInfo.date_created).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) + "</pre>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Due Date:         </strong> " + (ticketInfo.due_date ? new Date(ticketInfo.due_date).toLocaleDateString('en-US', { dateStyle: 'long'}) + ', midnight' : '-') + "</pre>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Last Checked:  </strong> " + (ticketInfo.last_checked ? new Date(ticketInfo.last_checked).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-') + "</pre>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Date Closed:    </strong> " + (ticketInfo.date_closed ? new Date(ticketInfo.date_closed).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) + "</pre><br>";
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Description:     </strong> " + ticketInfo.description + "</pre>";
          var currentTicket = ticketInfo.ticketNum;
	
          
          /*
          We know the following object will be the user who submitted the ticket
          */
          ticketTable.innerHTML += "<pre id='ticketInfo'><strong>Submitted by:  </strong> " + userInfo.username_id__username +  " (" + userGroup[userInfo.user_group] + ")</pre>";

          // /*
          // Loop through any remaining jsonReturn objects.  We know the fourth querty set contains
          // 1 or more techs assigned to the ticket.  We will pull these out first then comments
          // */
          for(var i = MIN_COMMENT_INDEX; i < jsonReturn.length; i++) {
            var obj = jsonReturn[i];
            // Grabs the techs from the json
            if(!obj.message) {
              ticketTable.innerHTML += "<p id='ticketInfo'><strong>Assigned Tech:</strong> " + obj.username_id__username +  " (" + userGroup[obj.user_group] + ")</p>";
            }
            // Grabs the comments from the json
            else {
              commentCount++
              ticketTable.innerHTML += "<br><p id='ticketInfo'><strong>Comment:</strong> "+ commentCount + "</p>";
              ticketTable.innerHTML += "<p id='ticketInfo'><strong>Message:</strong> " + obj.message + "</p>";
              ticketTable.innerHTML += "<p id='ticketInfo'><strong>From:</strong> " + obj.user__username +  " (" + userGroup[obj.user__profile__user_group] + ")</p>";
              ticketTable.innerHTML += "<p id='ticketInfo'><strong>Date Entered:</strong> " + (obj.date_entered ? new Date(obj.date_entered).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) + "</p>";
            }
          }

          //Lets user know if no tech is assigned to ticket
          if (!techAssigned){
            ticketTable.innerHTML += "<br><p id='ticketInfo'><strong><i>There is no tech assigned to this ticket</i></strong></p>";
          }

          // //Lets user know there are no comments
          if (commentCount == 0){
            ticketTable.innerHTML += "<br><p id='ticketInfo'><strong><i>There are no comments! Would you like to add one?</i></strong></p>";
          }
          // //Link to add comments to current ticket
          ticketTable.innerHTML += "<br><p id='ticketInfo'><strong><a class='link' href='/newcomment?ticketNum=" + currentTicket + "'>Add Comment</strong></a></p>";

          // // Hides assigning, opening and closing tickets from 'User'
          if (currentUserGroup == 'T') {
            ticketTable.innerHTML += "<br>"; 
            //close ticket
            if (ticketStatus == "Open") {
              ticketTable.innerHTML += "<p id='ticketInfo'><strong><a class='link' href='/close?ticketNum=" + currentTicket + "'>Close Ticket</strong></a></p>";
              //open ticket
            } else {
              ticketTable.innerHTML += "<p id='ticketInfo'><strong><a class='link' href='/open?ticketNum=" + currentTicket + "'>Re-Open Ticket</strong></a></p>";
            }

            if (isCurrentUserAssigned == "T") {
              //un-assign from ticket
              ticketTable.innerHTML += "<p id='ticketInfo'><strong><a class='link' href='/unassign?ticketNum=" + currentTicket + "'>Unassign from Ticket</strong></a></p>";
            } else {
              //assign to ticket
              ticketTable.innerHTML += "<p id='ticketInfo'><strong><a class='link' href='/assign?ticketNum=" + currentTicket + "'>Assign to Ticket</strong></a></p>";
            }
          }
        }
      }
  )
}

function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
}

function AllTickets(){
  let allTickets = "alltickets";
  let token = getCookie("csrftoken");
  console.log("test");

  $.ajax(
    {
        headers: { "X-CSRFToken": token },
        type:"POST",
        url: "/searchticket/",
        data:{
                 "alltickets": allTickets,
        },
        success: function( response ) 
        {
          BuildTable(response)
          let searchTicket = document.getElementById("ticketSearch");
          let status = document.getElementsByName("status")[0];
          let priority = document.getElementsByName("priority")[0];
          let assigned = document.getElementsByName("assigned")[0];

          status.value = "A";
          priority.value = "A";
          assigned.value = "A";
          searchTicket.value = "";

          console.log(status)
        }
      }
  )
  
}
function MyTickets(){
  let myTickets = "mytickets";
  let token = getCookie("csrftoken");

  $.ajax(
    {
        headers: { "X-CSRFToken": token },
        type:"POST",
        url: "/searchticket/",
        data:{
                 "mytickets": myTickets,
        },
        success: function( response ) 
        {
          BuildTable(response)
          let searchTicket = document.getElementById("ticketSearch");
          let status = document.getElementsByName("status")[0];
          let priority = document.getElementsByName("priority")[0];
          let assigned = document.getElementsByName("assigned")[0];

          status.value = "A";
          priority.value = "A";
          assigned.value = "A";
          searchTicket.value = "";

          console.log(status)
        }
      }
  )


}

function  TicketSearch(){

  let searchTicket = document.getElementById("ticketSearch");
  let status = document.getElementsByName("status")[0];
  let priority = document.getElementsByName("priority")[0];
  let assigned = document.getElementsByName("assigned")[0];
  console.log(status.value, priority.value, assigned.value)
  let token = getCookie("csrftoken");
  $.ajax(
    {
        headers: { "X-CSRFToken": token },
        type:"POST",
        url: "/searchticket/",
        data:{
                 post_id: searchTicket.value,
                 "status": status.value,
                 "priority": priority.value,
                 "assigned": assigned.value,
        },
        success: function( response ) 
        {
          BuildTable(response)
        }
      }
  )
}
function BuildTable(response){
          let jsonReturn = JSON.parse(response);
          let ticketTable = document.getElementById("ticketDiv");
          let status;
          let assigned;
          let priority;
          let mark;
          let innerHtml = '';
          if (jsonReturn.length == 0){
            innerHtml = "<h1><a href='#'> No Tickets Found</h1>"
          }
          for (var i = 0; i < jsonReturn.length; i++) 
          { 
            let ticketDiv = '<div onclick="getTicketInfo(' + jsonReturn[i]["ticketNum"] + ')" class="ticketInfo"><h3 class="subTicketHeaders">' + jsonReturn[i]["ticketNum"] + ' - ' + jsonReturn[i]["title"] + '</h3>';
            if (jsonReturn[i]["status"] == "O"){
              status = "Open";
            }else{''
              status = "Closed";
            }
            ticketDiv += '<p class="subTicketHeaders">Status: ' + status + '</p>'
            if (jsonReturn[i]["priority"] == "R"){
              priority = "Routine";
            }else if(jsonReturn[i]["priority"] == "U"){
              priority = "Urgent"
            }else{
              priority = "Emergency"
            }
             ticketDiv += '<p class="' + jsonReturn[i]["priority"] + '">Priority: ' + priority + '</p>'
             if (jsonReturn[i]["is_assigned"] == true){
              assigned = "True";
              mark = "&#x2713;"
            }else{
              assigned = "False"
              mark = "&#x2715;"
            }
/*  Assigned:<p class="assigned'+assigned+'">' + mark +'</p></h4>     */
            ticketDiv += '<p class="subTicketHeaders">Assigned:<b class="assigned'+assigned+'">' + mark 
            +'</b><p class="ticketP">Creation Date: ' + ((jsonReturn[i]["date_created"]) ? new Date(jsonReturn[i]["date_created"]).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) 
            +'</p><p class="ticketP">Due Date: ' + ((jsonReturn[i]["due_date"]) ? new Date(jsonReturn[i]["due_date"]).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) 
            + '</p><p class="ticketP">Last Checked: ' + ((jsonReturn[i]["last_checked"]) ? new Date(jsonReturn[i]["last_checked"]).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) : '-' ) + '</p></div>'
            innerHtml += ticketDiv;
          }
          ticketTable.innerHTML = innerHtml;

}
