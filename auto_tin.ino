#define STEPS 200
#define rev_len 10 // *0.1 mm
#define X_step 13
#define X_dir 12
#define Y_step 11
#define Y_dir 10
#define step_delay 1 //ms
#define in_step_delay 1000 //us
#define status_delay 1000 //ms
#define laser 3

int steps_x,steps_y;
int move_x,move_y;
unsigned long timer1,timer2;
byte laser_power;

void setup() {
  pinMode(X_step, OUTPUT);
  pinMode(X_dir, OUTPUT);
  pinMode(Y_step, OUTPUT);
  pinMode(Y_dir, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(50);
  Serial.println("Start");
  steps_x=0;
  steps_y=0;
  laser_power=0;
  timer1=0;
  timer2=0;
  pinMode(laser, OUTPUT);
}

void step_x(){
  if(steps_x>0){
    digitalWrite(X_dir,HIGH);
    digitalWrite(X_step,HIGH);
    delayMicroseconds(in_step_delay);
    digitalWrite(X_step,LOW);
    steps_x--;
  }
  else if(steps_x<0){
    digitalWrite(X_dir,LOW);
    digitalWrite(X_step,HIGH);
    delayMicroseconds(in_step_delay);
    digitalWrite(X_step,LOW);
    steps_x++;
  }
}

void step_y(){
  if(steps_y>0){
    digitalWrite(Y_dir,HIGH);
    digitalWrite(Y_step,HIGH);
    delayMicroseconds(in_step_delay);
    digitalWrite(Y_step,LOW);
    steps_y--;
  }
  else if(steps_y<0){
    digitalWrite(Y_dir,LOW);
    digitalWrite(Y_step,HIGH);
    delayMicroseconds(in_step_delay);
    digitalWrite(Y_step,LOW);
    steps_y++;
  }
}

void status_print(){
  Serial.print("Status: ");
  if(laser_power) Serial.print("TINNING laser_power: "+String(laser_power));
  else if((steps_x==0)&&(steps_y==0))Serial.print(("IDLE"));
  else {
    Serial.print("MOVING X: "+String((int)(rev_len*(steps_x/(float)STEPS)))+", Y: "+String((int)(rev_len*(steps_x/(float)STEPS))));
  }
  Serial.println();
}

void loop() {
  if(Serial.available()){
      move_x=Serial.parseInt();
      move_y=Serial.parseInt();
      steps_x=(move_x/(float)rev_len)*STEPS;
      steps_y=(move_y/(float)rev_len)*STEPS;
      laser_power=Serial.parseInt(); //0 to 255
      if((laser_power)&&((steps_x)||(steps_y))){
        Serial.println("ERROR: ACTIVE LASER WHILE MOVEMENT");
        Serial.println("Turning laser off");
        laser_power=0;
      }
      analogWrite(laser,laser_power);
  }
  if(millis()-timer1 > step_delay){
    timer1=millis();
    step_x();
    step_y();
  }

  if(millis()-timer2 > status_delay){
    timer2=millis();
    status_print();
  }
}
