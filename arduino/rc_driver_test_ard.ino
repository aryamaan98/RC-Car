int right_pin = 6;
int left_pin = 7;
int forward_pin = 10;

int time = 50;
int command = 0;

void setup(){
    pinMode(right_pin, OUTPUT);
    pinMode(left_pin, OUTPUT);
    pinMode(forward_pin, OUTPUT);
    pinMode(reverse_pin, OUTPUT);
    Serial.begin(115200); // rate = 115200
}
void loop() {
  // pi to arduino
  if (Serial.available() > 0){
    command = (Serial.read() - '0'); // char to integer
  }
  else{
    reset();
  }
   send_command(command,time);
}

void right(int time){
  digitalWrite(right_pin, HIGH);
  delay(time);
}

void left(int time){
  digitalWrite(left_pin, HIGH);
  delay(time);
}

void forward(int time){
  digitalWrite(forward_pin, HIGH);
  delay(time);
}

void forward_right(int time){
  digitalWrite(forward_pin, HIGH);
  digitalWrite(right_pin, HIGH);
  delay(time);
}

void forward_left(int time){
  digitalWrite(forward_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  delay(time);
}

void reset(){
  digitalWrite(forward_pin, LOW);
}

void send_command(int command, int time){
  switch (command){

     //reset command
     case 0: reset(); break;

     // single command
     case 1: forward(time); break;
     
     case 3: right(time); break;
     case 4: left(time); break;

     //combination command
     case 6: forward_right(time); break;
     case 7: forward_left(time); break;

     default: Serial.print("Invalid Command\n");
    }
}