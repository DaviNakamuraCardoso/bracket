# CS50 Web Programming Final Project: Bracket 

### Introduction 

[toc]

### Features

- Clinics should be able to:
  - [ ] Register their patients and doctors 
  - [ ] Send reminders and confirm appointments via 
    - [ ] The site
    - [ ] Email
    - [ ] WhatsApp
- Doctors should be able to:
  - [ ] Check the medical appointments for the day, week and month
  - [ ] Check the patient status
  - [ ] Take notes over patients
  - [ ] Create electronic transcriptions and records
- Patients should be able to: 
  - [ ] Schedule appointments
  - [ ] Confirm appointments 
  - [ ] Cancel appointments 

### History

- [12/2/2020] Initial setup
- [12/3/2020] GitHub Actions setup, PostgreSQL database setup
- 

<code>

function TestaCPF(strCPF) {
    var Soma;
    var Resto;
    Soma = 0;   
    //strCPF  = RetiraCaracteresInvalidos(strCPF,11);
    if (strCPF == "00000000000")
	return false;
    for (i=1; i<=9; i++)
	Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i); 
    Resto = (Soma * 10) % 11;
    if ((Resto == 10) || (Resto == 11)) 
	Resto = 0;
    if (Resto != parseInt(strCPF.substring(9, 10)) )
	return false;
	Soma = 0;
    for (i = 1; i <= 10; i++)
       Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
    Resto = (Soma * 10) % 11;
    if ((Resto == 10) || (Resto == 11)) 
	Resto = 0;
    if (Resto != parseInt(strCPF.substring(10, 11) ) )
        return false;
    return true;
}

</code>