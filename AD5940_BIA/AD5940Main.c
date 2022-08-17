/*!
 *****************************************************************************
 @file:    AD5940Main.c
 @author:  Neo Xu
 @brief:   Used to control specific application and process data.
 -----------------------------------------------------------------------------

Copyright (c) 2017-2019 Analog Devices, Inc. All Rights Reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.
By using this software you agree to the terms of the associated
Analog Devices Software License Agreement.
 
*****************************************************************************/
/** 
 * @addtogroup AD5940_System_Examples
 * @{
 *  @defgroup BioElec_Example
 *  @{
  */
#include "ad5940.h"
#include "AD5940.h"
#include <stdio.h>
#include "string.h"
#include "math.h"
#include "BodyImpedance.h"

#define APPBUFF_SIZE 512
uint32_t AppBuff[APPBUFF_SIZE];

int global_counter[2]={1,0};

/* It's your choice here how to do with the data. Here is just an example to print them to UART */
int32_t BIAShowResult(uint32_t *pData, uint32_t DataCount)
{
  float freq;

  fImpPol_Type *pImp = (fImpPol_Type*)pData;
  AppBIACtrl(BIACTRL_GETFREQ, &freq);
  float x,y, real, imag;
  for(int i=0;i<DataCount;i++)
  {


    y = pImp[i].Phase*180/MATH_PI;
    //if (y>270)
      //y = y - 360;
    real = pImp[i].Magnitude * cos(y);
    imag = pImp[i].Magnitude * sin(y);
    if (real<0)
      real = real * (-1);
    if (imag<0)
      imag = imag * (-1);
    x = pow(10,12)/(2*MATH_PI*freq*pImp[i].Magnitude);
    //printf("%3d    %6.0f    %8.0f    %3.0f    %2.4f\n", global_counter[0], freq, pImp[i].Magnitude, y, x-4.5);    //Padded, for terminal visualisation
    printf("%d,%.0f,%.0f,%.0f,%.4f,%.0f,%.0f\n", global_counter[0], freq, pImp[i].Magnitude, y, x, real,imag);    //For CSV
    //printf("%.0f   %.0f   %.0f   %.0f   %.0f\n",y,cos(y),sin(y),pImp[i].Magnitude * cos(y),pImp[i].Magnitude * sin(y));
  }
  return 0;
}

/* Initialize AD5940 basic blocks like clock */
static int32_t AD5940PlatformCfg(void)
{
  CLKCfg_Type clk_cfg;
  FIFOCfg_Type fifo_cfg;
  AGPIOCfg_Type gpio_cfg;

  /* Use hardware reset */
  AD5940_HWReset();
  /* Platform configuration */
  AD5940_Initialize();
  /* Step1. Configure clock */
  clk_cfg.ADCClkDiv = ADCCLKDIV_1;
  clk_cfg.ADCCLkSrc = ADCCLKSRC_HFOSC;
  clk_cfg.SysClkDiv = SYSCLKDIV_1;
  clk_cfg.SysClkSrc = SYSCLKSRC_HFOSC;
  clk_cfg.HfOSC32MHzMode = bFALSE;
  clk_cfg.HFOSCEn = bTRUE;
  clk_cfg.HFXTALEn = bFALSE;
  clk_cfg.LFOSCEn = bTRUE;
  AD5940_CLKCfg(&clk_cfg);
  /* Step2. Configure FIFO and Sequencer*/
  fifo_cfg.FIFOEn = bFALSE;
  fifo_cfg.FIFOMode = FIFOMODE_FIFO;
  fifo_cfg.FIFOSize = FIFOSIZE_4KB;                       /* 4kB for FIFO, The reset 2kB for sequencer */
  fifo_cfg.FIFOSrc = FIFOSRC_DFT;
  fifo_cfg.FIFOThresh = 4;//AppBIACfg.FifoThresh;        /* DFT result. One pair for RCAL, another for Rz. One DFT result have real part and imaginary part */
  AD5940_FIFOCfg(&fifo_cfg);                             /* Disable to reset FIFO. */
  fifo_cfg.FIFOEn = bTRUE;  
  AD5940_FIFOCfg(&fifo_cfg);                             /* Enable FIFO here */
  
  /* Step3. Interrupt controller */
  
  AD5940_INTCCfg(AFEINTC_1, AFEINTSRC_ALLINT, bTRUE);           /* Enable all interrupt in Interrupt Controller 1, so we can check INTC flags */
  AD5940_INTCCfg(AFEINTC_0, AFEINTSRC_DATAFIFOTHRESH, bTRUE);   /* Interrupt Controller 0 will control GP0 to generate interrupt to MCU */
  AD5940_INTCClrFlag(AFEINTSRC_ALLINT);
  /* Step4: Reconfigure GPIO */
  gpio_cfg.FuncSet = GP6_SYNC|GP5_SYNC|GP4_SYNC|GP2_TRIG|GP1_SYNC|GP0_INT;
  gpio_cfg.InputEnSet = AGPIO_Pin2;
  gpio_cfg.OutputEnSet = AGPIO_Pin0|AGPIO_Pin1|AGPIO_Pin4|AGPIO_Pin5|AGPIO_Pin6;
  gpio_cfg.OutVal = 0;
  gpio_cfg.PullEnSet = 0;

  AD5940_AGPIOCfg(&gpio_cfg);
  AD5940_SleepKeyCtrlS(SLPKEY_UNLOCK);  /* Allow AFE to enter sleep mode. */
  return 0;
}

/* !!Change the application parameters here if you want to change it to none-default value */
void AD5940BIAStructInit(int DataPoints, int RefreshFreq, int SweepEnable, int SweepStart, int SweepEnd, int LogScale)
{
  AppBIACfg_Type *pBIACfg;
  AppBIAGetCfg(&pBIACfg);
  
  pBIACfg->SeqStartAddr = 0;
  pBIACfg->MaxSeqLen = 512; /** @todo add checker in function */
  
  pBIACfg->RcalVal = 10000.0;
  pBIACfg->DftNum = DFTNUM_8192;
  pBIACfg->NumOfData = DataPoints;      /* Never stop until you stop it manually by AppBIACtrl() function */
  pBIACfg->BiaODR = RefreshFreq;         /* ODR(Sample Rate) 20Hz */
  pBIACfg->FifoThresh = 4;      /* 4 */
  pBIACfg->ADCSinc3Osr = ADCSINC3OSR_2;
  //pBIACfg->SinFreq = FixFreq;
  if(SweepEnable==1)
    pBIACfg->SweepCfg.SweepEn = bTRUE;
  else pBIACfg->SweepCfg.SweepEn = bFALSE;
  
  pBIACfg->SweepCfg.SweepStart = SweepStart;
  pBIACfg->SweepCfg.SweepStop = SweepEnd;
  pBIACfg->SweepCfg.SweepPoints = DataPoints;
  pBIACfg->SweepCfg.SweepIndex = 0;
  
  if(LogScale==1)
    pBIACfg->SweepCfg.SweepLog = bTRUE;
  else pBIACfg->SweepCfg.SweepLog = bFALSE;
  
  pBIACfg->SinFreq = pBIACfg->SweepCfg.SweepStart;
  global_counter[1] = pBIACfg->SweepCfg.SweepPoints;
}

void AD5940_Main(void)
{
  static uint32_t IntCount;
  //static uint32_t count;
  uint32_t temp;
  int c,d;
  AD5940PlatformCfg();
  AD5940BIAStructInit(100, 20, 1, 100, 199000, 1);  /*    int DataPoints
                                                               int RefreshFreq  --> recommended 20
                                                               
                                                               int SweepEnable  --> 0 or 1      
                                                               int SweepStart   --> ?? Minimum 100 Hz ??  Recommended 5000 Hz for real-time
                                                               int SweepEnd     --> Recommended max = 199 kHz
                                                               int LogScale                                       */
  while(1){
  //for(int i=1; i<=4; i++)
  //{
    AppBIAInit(AppBuff, APPBUFF_SIZE);    /* Initialize BIA application. Provide a buffer, which is used to store sequencer commands */
    AppBIACtrl(BIACTRL_START, 0);         /* Control BIA measurement to start. Second parameter has no meaning with this command. */
    //printf("\n        < Measurement %d/4 >\n---------------------------------------------------\n", i);
    global_counter[0]=1;
    while(global_counter[0] <= global_counter[1])
    {
      /* Check if interrupt flag which will be set when interrupt occurred. */
      if(AD5940_GetMCUIntFlag())
      {
        IntCount++;
        AD5940_ClrMCUIntFlag(); /* Clear this flag */
        temp = APPBUFF_SIZE;
        AppBIAISR(AppBuff, &temp); /* Deal with it and provide a buffer to store data we got */
        BIAShowResult(AppBuff, temp); /* Show the results to UART */
        global_counter[0]++;
        if(global_counter[0] > global_counter[1])
          {
            //IntCount = 0;
            //printf("---------------------------------------------------\nEnding sequence with %d successful measurements! :D \n--------------------------------------------------- \n", global_counter[0]-1);
            printf("end\n");
            for (c = 1; c <= 2500; c++)
              for (d = 1; d <= 2500; d++)
                {}
          }
      }
    }
  //}
  }
  //AppBIACtrl(BIACTRL_SHUTDOWN, 0);
}

/**
 * @}
 * @}
 * */
 