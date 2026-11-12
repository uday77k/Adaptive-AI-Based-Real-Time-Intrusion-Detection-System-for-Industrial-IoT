#include <LiquidCrystal.h>
#include <SPI.h>
#include <MFRC522.h>

// ================= LCD CONNECTIONS =================
int rs = 12;
int en = 13;
int d4 = 8;
int d5 = 9;
int d6 = 10;
int d7 = 11;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// ================= RFID RC522 CONNECTIONS =================
#define SS_PIN 10
#define RST_PIN 7

MFRC522 rfid(SS_PIN, RST_PIN);

// ================= AUTHORIZED RFID CARD =================
// Replace this example UID with your own card UID.
// Read the UID from the Serial Monitor.
byte authorizedUID[] = {0xDE, 0xAD, 0xBE, 0xEF};
const byte authorizedUIDSize = sizeof(authorizedUID);

bool cardAuthorized = false;

// ================= SETUP =================
void setup()
{
  Serial.begin(9600);

  // Initialize LCD
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("IOT INTRUDER");
  lcd.setCursor(0, 1);
  lcd.print("DETECTION SYSTEM");

  // Initialize RFID reader
  SPI.begin();
  rfid.PCD_Init();

  delay(2000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("RFID SYSTEM");
  lcd.setCursor(0, 1);
  lcd.print("SCAN YOUR CARD");

  Serial.println("IoT Intruder Detection System");
  Serial.println("Scan an RFID card...");
}

// ================= MAIN LOOP =================
void loop()
{
  SCANNING_CARD();
}

// ================= RFID CARD SCANNING =================
void SCANNING_CARD()
{
  // Check whether a new card is present
  if (!rfid.PICC_IsNewCardPresent())
  {
    return;
  }

  // Read card UID
  if (!rfid.PICC_ReadCardSerial())
  {
    return;
  }

  Serial.print("Card UID: ");

  for (byte i = 0; i < rfid.uid.size; i++)
  {
    Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(rfid.uid.uidByte[i], HEX);
  }

  Serial.println();

  // Check authorization
  cardAuthorized = checkAuthorizedCard();

  lcd.clear();

  if (cardAuthorized)
  {
    lcd.setCursor(0, 0);
    lcd.print("ACCESS GRANTED");

    lcd.setCursor(0, 1);
    lcd.print("WELCOME USER");

    Serial.println("Authorized Card");
    Serial.println("Access Granted");
  }
  else
  {
    lcd.setCursor(0, 0);
    lcd.print("UNAUTHORIZED!");

    lcd.setCursor(0, 1);
    lcd.print("INTRUDER ALERT");

    Serial.println("Unauthorized Card");
    Serial.println("Intruder Detected!");
  }

  delay(2500);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("RFID SYSTEM");
  lcd.setCursor(0, 1);
  lcd.print("SCAN YOUR CARD");

  // Stop communication with the current card
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}

// ================= AUTHORIZATION CHECK =================
bool checkAuthorizedCard()
{
  // The scanned UID length must match the stored UID
  if (rfid.uid.size != authorizedUIDSize)
  {
    return false;
  }

  for (byte i = 0; i < authorizedUIDSize; i++)
  {
    if (rfid.uid.uidByte[i] != authorizedUID[i])
    {
      return false;
    }
  }

  return true;
}
