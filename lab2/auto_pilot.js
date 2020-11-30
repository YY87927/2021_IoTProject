// ****************************************************
// Receive distance data as a string and parse the data to get distanceR and distanceL
// Use context.value to get uploaded data points
var raw_data = context.value;
var distance = raw_data.split(',');
var distanceR = parseFloat(distance[0]);
var distanceL = parseFloat(distance[1]);
// ****************************************************

// ****************************************************
// Determine which direction the automobile should go according to the two distance data
if (distanceR < 0.35 && distanceL < 0.35){
  var direction = 's';
}
else if (distanceR < 0.3 && distanceR < distanceL){
  var direction = 'a';
}
else if (distanceL < 0.3 && distanceL < distanceR){
 var direction = 'd' ;
}

else if (distanceR < 0.7 && distanceL < 0.7 && distanceR > distanceL){
  var direction = 'd';
}
else if (distanceR < 0.7 && distanceL < 0.7 && distanceL > distanceR){
  var direction = 'a';
}
else{
  var direction = 'w';
}
// ****************************************************

// ****************************************************
// Modify the data of other channels in the same MCS test device
return {
  distanceR: distanceR,
  distanceL: distanceL,
  direction: direction
};
