float stable_teta()
{
float tethaX, tethaY, tethaZ;

Get_Gyro_Val();
tethaX=(GYRO_X+pre_GYRO_X)*(-0.006717)*.0174; // (1/2)*T(0.005)*(Pi/180)=0.0000436
tethaY=(GYRO_Y+pre_GYRO_Y)*(-0.006717)*.0174;
tethaZ=(GYRO_Z+pre_GYRO_Z)*(-0.006717)*.0174;

pre_GYRO_X=GYRO_X;
pre_GYRO_Y=GYRO_Y;
pre_GYRO_Z=GYRO_Z;


R_gyro_X = R_est_X + (tethaX*tethaY-tethaZ)*R_est_Y + (tethaX*tethaZ+tethaY)*R_est_Z;
R_gyro_Y = (tethaZ)*R_est_X + (1+tethaY*tethaX*tethaZ)*R_est_Y + (tethaY*tethaZ-tethaX)*R_est_Z;
R_gyro_Z = (0-tethaY)*R_est_X + (tethaX)*R_est_Y + R_est_Z;

Get_Accel_Val();

R_est_X=(ACCELX*alpha + R_gyro_X*weight_gyro);
R_est_Y=(ACCELY*alpha + R_gyro_Y*weight_gyro);
R_est_Z=(ACCELZ*alpha + R_gyro_Z*weight_gyro);

Accel_Angle[X] = 57.295*atan((float) R_est_Y / sqrt(pow((float)R_est_Z,2)+pow((float)R_est_X,2)));
return (Accel_Angle[X]);
}