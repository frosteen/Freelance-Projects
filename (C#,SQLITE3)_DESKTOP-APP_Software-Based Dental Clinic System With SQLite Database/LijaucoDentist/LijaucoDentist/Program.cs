using System;
using System.Windows.Forms;

namespace LijaucoDentist
{
    static class Program
    {
        private static string password = "lijauco";
        public static DatabaseSQLite database = new DatabaseSQLite("DentalClinicDatabase.db", "admin");
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            try
            {
                database.MakeQuery(@"CREATE TABLE `AUTHENTICATION` (
	                `Type`	TEXT,
	                `Value`	TEXT,
                    PRIMARY KEY(`Type`)
                );");
                //DEFAULT USERNAMES & PASSWORDS
                database.INSERT("AUTHENTICATION", new string[] { "Type", "Value" },
                    new string[] { "Username", password });
                database.INSERT("AUTHENTICATION", new string[] { "Type", "Value" },
                    new string[] { "Password", password });
                database.MakeQuery(@"CREATE TABLE `PATIENTS` (
	                `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `Name`	TEXT,
	                `Birthday`	TEXT,
	                `Age`	TEXT,
	                `Status`	TEXT,
	                `Nationality`	TEXT,
	                `HomeAddress`	TEXT,
	                `Occupation`	TEXT,
	                `ParentGuardianName`	TEXT,
	                `OccupationParentGuardian`	TEXT,
	                `Sex`	TEXT,
	                `Nickname`	TEXT,
	                `HomeNo`	TEXT,
	                `OfficeNo`	TEXT,
	                `CelNo`	TEXT,
	                `Email`	TEXT,
	                `LastDentalVisit`	TEXT,
	                `NameOfPhysician`	TEXT,
	                `PhysicianSpecialty`	TEXT,
	                `PhysicianOfficeAddress`	TEXT,
	                `PhysicianOfficeNo`	TEXT,
	                `AreYouInAGoodHealth`	TEXT,
	                `MedicalTreatment`	TEXT,
	                `ConditionBeingTreated`	TEXT,
	                `SurgicalOperation`	TEXT,
	                `WhatIllnessOrOperation`	TEXT,
	                `EverBeenHospitalized`	TEXT,
	                `WhenAndWhy`	TEXT,
	                `AnyPrescription`	TEXT,
	                `PleaseSpecify`	TEXT,
	                `TobaccoProducts`	TEXT,
	                `AlcoholOrOtherDangerous`	TEXT,
	                `Allergic`	TEXT,
	                `BleedingTime`	TEXT,
	                `HaveOrHad`	TEXT,
	                `AreYouPregnant`	TEXT,
	                `AreYouNursing`	TEXT,
	                `BirthControlPills`	TEXT,
	                `BloodType`	TEXT,
	                `BloodPressure`	TEXT,
	                `PreviousDentist`	TEXT,
	                `Teeth`	TEXT
                );");
                database.MakeQuery(@"CREATE TABLE `RECORDS` (
	                `RecordID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	                `ID`	INTEGER,
	                `Date`	TEXT,
	                `Diagnosis`	TEXT,
	                `OralProphylaxis`	TEXT,
	                `Restorative`	TEXT,
	                `Surgery`	TEXT,
	                `Endodontic`	TEXT,
	                `OrthodonticMiscellaneous`	TEXT,
	                `Orthodontic`	TEXT,
	                `ProsthodonticsRemovable`	TEXT,
	                `ProsthodonticsFixed`	TEXT,
	                `ProsthodonticsPontics`	TEXT,
	                `ProsthodonticsRepair`	TEXT,
	                `ProsthodonticsOthers`	TEXT,
	                `TMJ`	TEXT,
	                `DiagnosisToothNo`	TEXT,
	                `RestorativeToothNo`	TEXT,
	                `SurgeryToothNo`	TEXT,
	                `EndodonticToothNo`	TEXT,
	                `ProsthodonticsRemovableToothNo`	TEXT,
	                `ProsthodonticsFixedToothNo`	TEXT,
	                `ProsthodonticsRepairToothNo`	TEXT,
	                `AmountPaid`	TEXT,
	                `AmountCharged`	TEXT,
	                `Balance`	TEXT,
	                `Notes`	TEXT
                );");
            }
            catch
            {
                database.sqlite_conn.Close();
            }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            //Application.Run(new AdminUI());
            Application.Run(new LoginUI(new AdminUI(), true));
        }
    }
}
