// Version 0.1
//0 = no key pressed;
//1 = UP key pressed;
//2 = DOWN key pressed;
//3 = LEFT key pressed;
//4 = RIGHT key pressed;


int pinForward = 10;
int pinRevers  = 9;
int pinRight   = 11;
int pinLeft    = 12;


int maxN=1;
int cmd=0;

int FR=0; // -3,-2,-1, 0, 1, 2, 3
int LR=0;
  
  
void setup()
{
  Serial.begin(9600);  
  
  pinMode(pinForward, OUTPUT);  
  digitalWrite(pinForward, LOW);
  
  pinMode(pinRevers, OUTPUT);  
  digitalWrite(pinRevers, LOW);

  pinMode(pinRight, OUTPUT);  
  digitalWrite(pinRight, LOW);

  pinMode(pinLeft, OUTPUT);  
  digitalWrite(pinLeft, LOW);


  Serial.println("RESET");  
  
  
  FR=0; 
  LR=0;

  
}


void loop()
{ 

  if (Serial.available() > 0) {  
    cmd = Serial.read(); 
    
    if (cmd>47){
                 cmd = cmd-48;
               }
    
    switch (cmd) { 
      case 1:
              if (FR<maxN){ FR=FR+1; }
              SetPinAct(FR,pinForward,pinRevers);
              Serial.println("1:Forward");  
              break;  
      case 2:
              if (FR>-maxN){ FR=FR-1; }
              SetPinAct(FR,pinForward,pinRevers);
              Serial.println("2:Revers"); 
              break;  


      case 3:
              if (LR<maxN){ LR=LR+1; }
              SetPinAct(LR,pinLeft,pinRight);
              break;  
      case 4:
              if (LR>-maxN){ LR=LR-1; }
              SetPinAct(LR,pinLeft,pinRight);
              break;  

      default: 
              Serial.print("DEFAULT:"); 
              Serial.println(cmd);
    }

  }

}

void SetPinAct(int Flag, int pin1, int pin2){
  if (Flag>0) {
     digitalWrite(pin1, HIGH); 
     digitalWrite(pin2, LOW);
  }
  if (Flag==0) {
     digitalWrite(pin1, LOW); 
     digitalWrite(pin2, LOW);
  }
  if (Flag<0) {
     digitalWrite(pin1, LOW); 
     digitalWrite(pin2, HIGH);
  }

}
