
/*
#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 24                       #
#    For:         Ista Sanat Co.                    #
#    File:        Alarm Main Controller             #
#####################################################
*/

// Needed Header Files
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/background_segm.hpp>
#include <vector>
#include <thread>
#include <opencv2/xphoto/white_balance.hpp>
#include "Tracking.h"
#include "TrackingSmoke.h"
#include <cctype>
#include <string>
#include <stdio.h>
#include <csignal>
//RPi Headers
#include <raspicam/raspicam_cv.h>
#include <chrono>
#include <ctime>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <wiringPi.h>

using namespace std;
using namespace cv;
using namespace cv::xphoto;

//Set-up LK OpticalFlow
Tracking tracking;
TrackingSmoke trackingSmoke;


//Public Variables for set trackbar amounts*
int frameWidth = 0;
int frameHeight = 0;
int thrFirstFrame = 40;
int claheValue = 1;
float alpha = 0.02;
bool maybeFlame = false;
bool maybeSmoke = false;
bool firstStepFlameDet = false;
bool firstStepSmokeDet = false;
long int smokeArea = 0;
long int flameArea = 0;
long int smokeOmega = 0;
int smokeFrameCNT = 1;
int flameFrameCNT = 0;
float f0 = 0, fv = 0;
vector<float> f ;
vector<float> zeroF;
vector<Point2f> zeroPoints;
Mat frame, frameOrg, b, thr;
Mat test, test1;
int frameLED = 21;
bool frameBool = false;

// Motion Return Struc.
struct motionBack
{
	vector<Mat> MATVEC;
	int FCNT;
};

motionBack mdVec;
motionBack mdVec_;

//BackgroundSubtract
Ptr< BackgroundSubtractor> pMOG2;

int itest = 0;

bool modeFire = false;
bool shotFire = false;
bool shotmaybeFire = false;
bool shotmaybeSmoke = false;
bool shotprealarm = false;
string shotFireFile;
string shotmaybeFireFile;

int flameCNT = 0;
int maybeFlameCNT = 0;

clock_t startFireTimer = clock();
clock_t startmaybeFireTimer = clock();
clock_t startmaybeSmokeTimer = clock();
clock_t startpreAlarmTimer = clock();

// Variables and kernels for erode and dilate
// Variables and kernels for erode and dilate
Mat flameClosingKernel = getStructuringElement(MORPH_ELLIPSE, Size(3, 3));
Mat flameOpeningKernel = getStructuringElement(MORPH_ELLIPSE, Size(3, 3));
Mat smokeDilateKernel = getStructuringElement(MORPH_RECT, Size(3, 3));
Mat smokeErodeKernel = getStructuringElement(MORPH_RECT, Size(3, 3));


//Variables for settings
bool fmMode = false;
bool smMode = false;
bool alMode = false;
bool voMode = false;

//Restart System after divided By Zero
void handler(int a) {
    cout << "Signal " << a << " here!" << endl;
    if(a==8)
    {
		system("sudo reboot");
	}
}


// Write Output
void changemode()
{
	int fireFileCNT = 1;
	int smokeFileCNT = 1;
	while(true)
	{
		if (shotmaybeFire == true)
		{
			double duration = (clock() - startmaybeFireTimer) / (double) CLOCKS_PER_SEC;
			if (duration > 20.0)
			{
				startmaybeFireTimer = clock();
				
				// Save Output Frame
				stringstream fireFileName;
				fireFileName << "/home/pi/IS/webserver/DB/frameCacheFire" << fireFileCNT << ".jpg";
				imwrite(fireFileName.str(),frame);
				fireFileCNT++;
				
				if (fireFileCNT == 10)
				{
					fireFileCNT = 1;
				}
				
				// For old version
				/*stringstream cmnd;
				cmnd << "python3 /home/pi/Desktop/fireAlarm.py maybeFire " << shotmaybeFireFile;
				system(cmnd.str().c_str());*/
			}
			shotmaybeFire = false;
		}
		
		if (shotmaybeSmoke == true)
		{
			double duration = (clock() - startmaybeSmokeTimer) / (double) CLOCKS_PER_SEC;
			if (duration > 20.0)
			{
				startmaybeSmokeTimer = clock();
				
				// Save Output Frame
				stringstream smokeFileName;
				smokeFileName << "/home/pi/IS/webserver/DB/frameCacheSmoke" << smokeFileCNT << ".jpg";
				imwrite(smokeFileName.str(),frame);
				//smokeFileCNT++;
				
				if (smokeFileCNT == 10)
				{
					smokeFileCNT = 1;
				}
				
				// For old version
				/*stringstream cmnd;
				cmnd << "python3 /home/pi/Desktop/fireAlarm.py maybeFire " << shotmaybeFireFile;
				system(cmnd.str().c_str());*/
			}
			shotmaybeSmoke = false;
		}
		if (shotprealarm == true)
		{
			double duration = (clock() - startpreAlarmTimer) / (double) CLOCKS_PER_SEC;
			if (duration > 20.0)
			{
				startpreAlarmTimer = clock();
				
				cerr << "OK";
				
				// Save Output Frame
				time_t rawtime;
			    struct tm * timeinfo;
			    char buffer[80];
			    time (&rawtime);
			    timeinfo = localtime(&rawtime);
			    strftime(buffer,sizeof(buffer),"%Y%m%d_%H%M%S",timeinfo);
			    string str(buffer);
			    stringstream preAlarmFileName;
				preAlarmFileName << "/home/pi/IS/webserver/IMG_DB/prealarm_" << str << ".jpg";
				imwrite(preAlarmFileName.str(),frame);
				
				
				// Send Pre-Alarm
				stringstream cmnd;
				cmnd << "python3 /home/pi/IS/alarm.py -event=prealarm -filename=prealarm_" << str <<".jpg";
				system(cmnd.str().c_str());
			}
			shotprealarm = false;
		}
	}
}


//Balancing Illumination (1st Block - Convert to LAB Color format)
Mat labColorFormat(Mat input)
{
	//Create Some mat
	Mat labFrame;
	//Convert input frame to LAB Format
	cvtColor(input, labFrame, CV_BGR2Lab);
	//Split Color Channels
	vector<Mat> labChs(3);
	split(labFrame, labChs);
	//Apply CLAHE algorithim to L channel
	Ptr<CLAHE> clahe = createCLAHE();
	clahe->setClipLimit(claheValue);
	Mat labOut;
	clahe->apply(labChs[0], labOut);
	//Back changed Channel in main channel mat
	labOut.copyTo(labChs[0]);
	merge(labChs, labFrame);
	//Back to BGR Color Format
	Mat output;
	cvtColor(labFrame, output, CV_Lab2BGR);

	return output;

}

//Balancing Color (1st Block - Gray-World Method)
Mat grayWorld(Mat imgIn, string mode) {
	Mat imgOut;

	//Sum the colour values in each channel
	Scalar sumImg = sum(imgIn);
	//normalise by the number of pixels in the image to obtain an extimate for the illuminant
	Scalar illum = sumImg / (imgIn.rows*imgIn.cols);
	// Split the image into different channels
	vector<Mat> rgbChannels(3);
	split(imgIn, rgbChannels);
	//Assign the three colour channels to Mat variables for processing
	Mat redImg = rgbChannels[2];
	Mat graanImg = rgbChannels[1];
	Mat blueImg = rgbChannels[0];
	//calculate scale factor for normalisation you can use 255 instead
	double scale = (illum(0) + illum(1) + illum(2)) / 3;
	//correct for illuminant (white balancing)
	redImg = redImg*scale / illum(2);
	graanImg = graanImg*scale / illum(1);
	blueImg = blueImg*scale / illum(0);
	//Assign the processed channels back into vector to use in the merge() function
	rgbChannels[0] = blueImg;
	rgbChannels[1] = graanImg;
	rgbChannels[2] = redImg;

	//to hold the output image, Merge the processed colour channels
	merge(rgbChannels, imgOut);
	return imgOut;
}

//Motion Detection (2nd Block, Basic math for motion detection)
motionBack motionDetection(Mat fT, Mat fT1, Mat fT2, Mat b, Mat thr)
{
	// Create some variable for calculation
	int infT, infT1, infT2, inb, d1, d2, d3;
	int bb, cc;
	motionBack output;
	output.FCNT = 0;
	Mat F(fT.rows, fT.cols, CV_8UC1);
	Mat bt1(fT.rows, fT.cols, fT.type());
	Mat thrt1(fT.rows, fT.cols, CV_8UC1);
	
	// Calculate I(i,j;t)
	Mat fTG;
	cvtColor(fT, fTG, CV_BGR2GRAY);
	// Calculate I(i,j;t-1)
	Mat fT1G;
	cvtColor(fT1, fT1G, CV_BGR2GRAY);
	//Calculate I(i,j;t-2)
	Mat fT2G;
	cvtColor(fT2, fT2G, CV_BGR2GRAY);
	// Calculate B(i,j;t)
	Mat bG = b.clone();
	//cvtColor(b, bG, CV_BGR2GRAY);
	
	// Get each frame in Four frames
	for (int i=0; i < fT.rows; i++)
	{
		for (int j = 0; j < fT.cols; j++)
		{
			// Calculate I(i,j;t)
			infT = fTG.at<uchar>(i, j);
			// Calculate I(i,j;t-1)
			infT1 = fT1G.at<uchar>(i, j);
			//Calculate I(i,j;t-2)
			infT2 = fT2G.at<uchar>(i, j);
			// Calculate B(i,j;t)
			inb = bG.at<uchar>(i, j);
			// Calculate D1(i,j,t), D2(i,j,t), D3(i,j,t)
			//#^#
			d1 = abs(infT - infT1);
			d2 = abs(infT - infT2);
			d3 = abs(infT - inb);
			//Calculate binary output for Motion Detection and put results in F(i,j,t)
			//#^#
			if ((d1 > (int)thr.at<uchar>(i, j)) && (d2 > (int)thr.at<uchar>(i, j)) && (d3 > (int)thr.at<uchar>(i, j)))
			{
				F.at<uchar>(i, j) = 255;
				output.FCNT++;
			}
			else
			{
				F.at<uchar>(i, j) = 0;
			}
			//Calculate B(i,j;t+1)
			if ((int)F.at<uchar>(i, j) == 0)
			{
				bb = (alpha * inb) + ((1 - alpha)*infT);
				bt1.at<Vec3b>(i, j)[0] = bb;
				bt1.at<Vec3b>(i, j)[1] = bb;
				bt1.at<Vec3b>(i, j)[2] = bb;
			}
			else
			{
				bb = inb;
				bt1.at<Vec3b>(i, j)[0] = bb;
				bt1.at<Vec3b>(i, j)[1] = bb;
				bt1.at<Vec3b>(i, j)[2] = bb;
			}
			//Calculate T(i,j;t+1)
			if ((int)F.at<uchar>(i, j) == 255)
			{
				cc = (alpha * (int)thr.at<uchar>(i, j)) + ((1 - alpha)*abs(infT - bb));
				thrt1.at<uchar>(i, j) = cc;
			}
			else
			{
				cc = (int)thr.at<uchar>(i, j);
				thrt1.at<uchar>(i, j) = cc;
			}
		}
	}
	output.MATVEC.push_back(F);
	output.MATVEC.push_back(bt1);
	output.MATVEC.push_back(thrt1);
	return output;
}

void ImgMean(float& c1, float& c2, float& c3, Mat pImg)
{
	int nPixel = pImg.rows*pImg.cols;	// number of pixels in image
	c1 = 0; c2 = 0; c3 = 0;

	MatConstIterator_<Vec3b> it = pImg.begin<Vec3b>();
	MatConstIterator_<Vec3b> itend = pImg.end<Vec3b>();

	while (it != itend)
	{
		c1 += (*it)[0];
		c2 += (*it)[1];
		c3 += (*it)[2];
		it++;

	}

	c1 = c1 / nPixel;
	c2 = c2 / nPixel;
	c3 = c3 / nPixel;
}

// Determine which sections are in Flame Color limitation (3th Block - Flame Color Model)
Mat flameColorDet() {
	
	Mat output(frame.rows, frame.cols, CV_8UC1);
	
	//Mat m_pcurFrameYCrCb(frame.rows, frame.cols, frame.type());
	//m_pcurFrameYCrCb = frame.clone();
	//float yy_mean = 0, cr_mean = 0, cb_mean = 0;
	//ImgMean(cb_mean, cr_mean, yy_mean, m_pcurFrameYCrCb);
	uchar yy = 0, cr = 0, cb = 0;
	
	
	float r, g, b, h, s, in, m, n;

	Mat frameG;
	cvtColor(frame, frameG, CV_BGR2GRAY);
	
	for (int i = 0; i < frame.rows; i++)
	{
		for (int j = 0; j < frame.cols; j++)
		{
			int B = frame.at<Vec3b>(i, j)[0];
			int G = frame.at<Vec3b>(i, j)[1];
			int R = frame.at<Vec3b>(i, j)[2];
			
			//cb = m_pcurFrameYCrCb.at<Vec3b>(i, j)[0];
			//cr = m_pcurFrameYCrCb.at<Vec3b>(i, j)[1];
			//yy = m_pcurFrameYCrCb.at<Vec3b>(i, j)[2];
			
			if (B == 0 && G == 0 && R == 0)
			{
				B=1;
				G=1;
				R=1;
			}
			
			b = B / (B + G + R);
			g = G / (B + G + R);
			r = R / (B + G + R);

			// Calculate I
			in = frameG.at<uchar>(i,j);

			float min_val = 0;
			min_val = min(r, min(b, g));

			//Calculate S
			s = 1 - (3 * (min_val));

			//Condition for min & max value of S
			if (s < 0.00001)
			{
				s = 0;
			}
			else if (s > 0.99999)
			{
				s = 1;
			}

			//Condition about S not equal ZERO
			h = 0;
			if (s != 0)
			{
				h = (0.5*((R - G) + (R - B))) / (sqrt(((R - G)*(R - G)) + ((R - B)*(G - B))));
				h = acos(h);

				if (B <= G)
				{
					h = h;
				}
				else {
					h = (2 * CV_PI) - h;
				}
			}

			//Calculate Degress from Radian
			float h_deg = (h*180.0) / CV_PI;
			float s_con = (255.0 - R) * (0.7 / 230.0);
			
			//if (R>120 && yy>cb&&cr>cb&&yy>yy_mean && (abs(cb - cr)>40))
			if ((R > 230 && R >= G && G > B) && (h_deg >= 0 && h_deg <= 60) && (s >= s_con) && (in >= 150) /*&& (s >= 0.3 && s <= 0.7)*/ )
			//if (R > 230 && R >= G && G >= B && s > s_con && in >=150)
			{
				output.at<uchar>(i, j) = 255;
			}
			else
			{
				output.at<uchar>(i, j) = 0;
			}
		}
	}
	return output;
}

//check intensity in two sequence of frames
Mat smokeIntensity(Mat fT_, Mat fT1_, Mat fT2_)
{
	Mat output = Mat::zeros(frame.rows, frame.cols, CV_8UC1);
	for (int i = 0; i < frame.rows; i++)
	{
		for (int j = 0; j < frame.cols; j++)
		{
			// Get BGR value of Current Frame
			int BfT_ = fT_.at<Vec3b>(i, j)[0];
			int GfT_ = fT_.at<Vec3b>(i, j)[1];
			int RfT_ = fT_.at<Vec3b>(i, j)[2];
			int inT = (BfT_ + GfT_ + RfT_) / (3.0);
			// Get BGR value of previous Frame
			int BfT1 = fT1_.at<Vec3b>(i, j)[0];
			int GfT1 = fT1_.at<Vec3b>(i, j)[1];
			int RfT1 = fT1_.at<Vec3b>(i, j)[2];
			int inT1 = (BfT1 + GfT1 + RfT1) / (3.0);
			// Determine Color Change for Smoke regions
			if ((inT - inT1) < 100 && (inT - inT1) > 50)
			{
				output.at<uchar>(i, j) = 255;
			}
		}
	}
	return output;
}


// Determine which sections are in Smoke Color limitation (3th Block - Smoke Color Model)
Mat smokeColorDet() {
	Mat output(frame.rows, frame.cols, CV_8UC1);
	float r, g, b, s, in, h;
	for (int i = 0; i < frame.rows; i++)
	{
		for (int j = 0; j < frame.cols; j++)
		{
			int B = frame.at<Vec3b>(i, j)[0];
			int G = frame.at<Vec3b>(i, j)[1];
			int R = frame.at<Vec3b>(i, j)[2];

			if (B == 0 && G == 0 && R ==0)
			{
				B=1;
				G=1;
				R=1;
			}
			
			b = B / (B + G + R);
			g = G / (B + G + R);
			r = R / (B + G + R);

			// Calculate I
			in = (B + G + R) / (3.0);

			float min_val = 0;
			min_val = min(r, min(b, g));

			//Calculate S
			s = 1 - (3 * (min_val));

			//Condition for min & max value of S
			if (s < 0.001)
			{
				s = 0;
			}
			else if (s > 0.999)
			{
				s = 1;
			}

			float m = max(B, max(G, R));
			float n = min(B, min(G, R));

			//if (abs(R-G) < 10 && abs(G-B) < 10 && abs(R-B) < 10 && (in>80) && (in<255))
			bool rule1 = m - n < 10.0;
			bool rule2 = (in > 80) && (in < 255);
			bool rule3 = (m == B) && (m - n < 10.0);
			bool rule4 = abs(R - G) < 10 && abs(G - B) < 10 && abs(R - B) < 10;
			bool rule5 = R > 150 && G > 150 && B > 150;
			if (rule1 && rule5 && rule4 && rule2)
			{
				//cout << B << "\t" << G << "\t" << R << endl;
				output.at<uchar>(i, j) = 255;
			}
			else
			{
				output.at<uchar>(i, j) = 0;
			}
		}
	}
	return output;
}


//Interest Regions Detection with Connected Component Alghorithm (4th Step - smoke)
void smokeConnectedComponentsstats(Mat img)
{
	firstStepSmokeDet = false;
	long int currentArea = 0;
	float currentOmega = 0;
	//use connectedcomponentsStats
	Mat labels, stats, centroids;
	int num_objects = connectedComponentsWithStats(img, labels, stats, centroids);
	for (int i = 1; i < num_objects; i++)
	{
		float perimeter_i = stats.at<int>(i, CC_STAT_HEIGHT) * stats.at<int>(i, CC_STAT_WIDTH);
		currentOmega = currentOmega + ((perimeter_i) / (2 * sqrt(CV_PI * stats.at<int>(i, CC_STAT_AREA))));
		currentArea = currentArea + stats.at<int>(i, CC_STAT_AREA);
	}
	if ((currentOmega - smokeOmega > 2.0 ) && (currentArea - smokeArea < 100.0))
	{
		/*for (int i = 1; i < num_objects; i++)
		{
			// Draw Rect around Smoke Sections
			Rect smokeBox;
			smokeBox.x = stats.at<int>(i, CC_STAT_LEFT);
			smokeBox.y = stats.at<int>(i, CC_STAT_TOP);
			smokeBox.height = stats.at<int>(i, CC_STAT_HEIGHT);
			smokeBox.width = stats.at<int>(i, CC_STAT_WIDTH);
			//rectangle(frameOrg, smokeBox, Scalar(0, 255, 255), 3);
		}
		putText(frameOrg, "SMOKE", Point(50, 10), FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 255, 255), 2);*/
		firstStepSmokeDet = true;
	}
	if (currentArea > 0 && maybeSmoke == false)
	{
		maybeSmoke = true;
	}
	if (currentArea > 0)
	{
		smokeFrameCNT++;
	}
	else
	{
		maybeSmoke = false;
		smokeArea = 0;
		trackingSmoke.ProcessKey('c');
		smokeFrameCNT = 0;
	}
	smokeArea = currentArea;
	smokeOmega = currentOmega;
}


//Interest Regions Detection with findContours Alghorithm (4th Step - smoke)
Mat findContoursBasic(Mat img)
{
	vector<vector<Point>> contours;
	findContours(img, contours, RETR_EXTERNAL, CHAIN_APPROX_TC89_L1);
	Mat output = Mat::zeros(img.rows, img.cols, CV_8UC3);
	//check the number of objects
	if (contours.size() == 0)
	{
	cout << "No Objects detected" << endl;
	}
	else
	{
	cout << "Number of objects detected: " << contours.size() << endl;
	}
	RNG rng(0xFFFFFFFF);
	for (int i = 0; i<contours.size(); i++)
		drawContours(output, contours, i, Scalar(0,0,255));
	return output;
}


//Interest Regions Detection with Connected Component Alghorithm (4th Step - flame)
void flameConnectedComponentsstats(Mat img)
{
	firstStepFlameDet = false;
	//use connectedcomponentsStats
	Mat labels, stats, centroids;
	long int currentFlameArea = 0;
	int num_objects = connectedComponentsWithStats(img, labels, stats, centroids);

	for (int i = 1; i < num_objects; i++)
	{

		//draw text with area
		/*stringstream ss;
		ss << "%%";
		putText(frameOrg, ss.str(), centroids.at<Point2d>(i), FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 0, 255), 2);
		*/
		// Draw a rectangle around Flame section
		Rect flameBox;
		flameBox.x = stats.at<int>(i, CC_STAT_LEFT);
		flameBox.y = stats.at<int>(i, CC_STAT_TOP);
		flameBox.height = stats.at<int>(i, CC_STAT_HEIGHT);
		flameBox.width = stats.at<int>(i, CC_STAT_WIDTH);
		currentFlameArea += flameBox.area();
		rectangle(frameOrg, flameBox, Scalar(0, 0, 255), 3);
	}
	if (maybeFlame == false && currentFlameArea > 0)
	{
		flameArea = currentFlameArea;
		maybeFlame = true;
		//size(f = vector<float>(f.size(), 0));
	}
	else if (currentFlameArea > 0 && maybeFlame == true && currentFlameArea > flameArea)
	{
		//Save Flame Pic.
		/*stringstream pics;
		auto fTime = chrono::system_clock::now();
		time_t FTime = chrono::system_clock::to_time_t(fTime);
		pics << "/home/pi/database/MayBeFLAME_" <<ctime(&FTime) << ".jpg";
		pics << "/home/pi/database/MayBeFLAME_" << maybeFlameCNT << ".jpg";*/
		
		if (maybeFlameCNT == 100)
			maybeFlameCNT =0;
		else
			maybeFlameCNT++;
		//shotmaybeFireFile = pics.str();
		shotmaybeFire=true;
		firstStepFlameDet = true;
		putText(frameOrg, "FLAME", Point(3,10), FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 0, 255), 2);
		//imwrite(pics.str(), frameOrg);
		
	}
	
	if (currentFlameArea == 0)
	{
		maybeFlame = false;
		flameArea = 0;
		tracking.ProcessKey('c');
	}
	if (currentFlameArea > 0)
	{
		flameFrameCNT++;
	}
	else
	{
		flameFrameCNT = 0;
		f0 = 0;
		fv = 0;
		f = zeroF;
		tracking.ProcessKey('c');
	}

	//cout << maybeFlame << "\t" << currentFlameArea <<"\t" <<flameArea << endl;
}


//Absolute Color Change for Detect Smoke Section of each frame (5th Step - Smoke)
Mat absoluteColorChange(Mat smokecandidate, Mat fT_, Mat fT1_)
{
	Mat output = Mat::zeros(frame.rows, frame.cols, CV_8UC1);

	for (int i = 0; i < frame.rows; i++)
	{
		for (int j = 0; j < frame.cols; j++)
		{
			if (smokecandidate.at<uchar>(i,j) == 255)
			{
				// Get BGR value of Current Frame
				int BfT_ = fT_.at<Vec3b>(i, j)[0];
				int GfT_ = fT_.at<Vec3b>(i, j)[1];
				int RfT_ = fT_.at<Vec3b>(i, j)[2];
				// Get BGR value of previous Frame
				int BfT1_ = fT1_.at<Vec3b>(i, j)[0];
				int GfT1_ = fT1_.at<Vec3b>(i, j)[1];
				int RfT1_ = fT1_.at<Vec3b>(i, j)[2];
				//Diff of Colors
				int gD = abs(GfT_ - GfT1_);
				int rD = abs(RfT_ - RfT1_);
				int bD = abs(BfT_ - BfT1_);
				// Determine Color Change for Smoke regions
				if (gD < 10 && rD < 10 && bD < 10 && (gD == rD) &&(gD == bD))
				{
					output.at<uchar>(i, j) = 255;
				}
			}
		}
	}
	return output;
}


//Optical FLow for estimate motion in a candidate flame region (6th Block - Flame)
void flameOpticalFlow(Mat input)
{
	vector<vector<Point2f>> points;
	if (flameFrameCNT == 1)
	{
		tracking.ProcessKey('r');
	}
	if (flameFrameCNT > 1)
	{
		points = tracking.Process(input);
		tracking.Draw(frameOrg);
		vector<Point2f> currentPoints;
		vector<Point2f> previousPoints;
		//Put Points in seperate vectors
		previousPoints = points[1];
		currentPoints = points[0];
		float maxPoints = currentPoints.size();
		//cout << previousPoints << endl;
		//cout << currentPoints << endl;
		if (flameFrameCNT == 3)
		{
			for (int m = 0; m < maxPoints; m++)
			{
				f0 = f0 + (sqrt((previousPoints[m].y - currentPoints[m].y)*(previousPoints[m].y - currentPoints[m].y) +
					(previousPoints[m].x - currentPoints[m].x)*(previousPoints[m].x - currentPoints[m].x)));
			}
			f0 = f0 * (1 / maxPoints);
			//cout << "F0= " << f0 << endl;
		}
		else if (flameFrameCNT > 3)
		{
			float cacheF = 0;
			for (int m = 0; m < maxPoints; m++)
			{
				cacheF = cacheF + (sqrt((previousPoints[m].y - currentPoints[m].y)*(previousPoints[m].y - currentPoints[m].y) +
					(previousPoints[m].x - currentPoints[m].x)*(previousPoints[m].x - currentPoints[m].x)));
			}
			cacheF = cacheF * (1 / maxPoints);
			f.push_back(cacheF);
			//cout << "F= " << cacheF << endl;
			
			float upDirection = 0;
			float deltaY = 0, deltaX = 0;
			for (int m = 0; m < maxPoints; m++)
			{
				deltaY = currentPoints[m].y - previousPoints[m].y;
				deltaX = currentPoints[m].x - previousPoints[m].x;
				//cout << "X\t" << deltaX << endl;
				//cout << "Y\t" << deltaY << endl;
				if (deltaY < 0 && abs(deltaY / deltaX) > 1.5)
				{
					upDirection++;
				}
			}
			//cout << "++++++++++++++++++\t" << maxPoints << endl;
			//cout << 100 * (upDirection / maxPoints) << " %" << endl;

			if (f.size() > 1)
			{
				float cacheFv = 0;
				for (int i = 0; i < f.size(); i++)
				{
					cacheFv = cacheFv + (f[i] - f0);
				}
				fv = (1 / ((float)f.size() - 1)) * cacheFv;
				cerr << "FV= " << fv << "\t" << f.size() << endl;
				if ((100 * (upDirection / maxPoints)) > 50.0 && abs(fv) > 5.0 && abs(fv) < 150.0 && f.size() > 4 && firstStepFlameDet)
				{
					//Save Flame Pic.
					/*stringstream pics;
					auto fTime = chrono::system_clock::now();
					time_t FTime = chrono::system_clock::to_time_t(fTime);
					pics << "/home/pi/database/FLAME_" <<ctime(&FTime) << ".jpg";
					pics << "/home/pi/database/MayBeFLAME_" << flameCNT << ".jpg";*/
					if (flameCNT == 100)
						flameCNT =0;
					else
						flameCNT++;
					//shotFireFile = pics.str();
					//shotFire = true;
					//modeFire = true;
					putText(frameOrg, "FLAME", Point(3, 30), FONT_HERSHEY_SIMPLEX, 0.4, Scalar(255, 0, 0), 2);
					shotprealarm = true;
					//imwrite(pics.str(), frameOrg);
				}
			}
		}
	}
}


//Optical FLow for estimate motion in a candidate Smoke region (Added Block - Smoke)
void smokeOpticalFlow(Mat input)
{
		vector<vector<Point2f>> pointsSmoke;
	if (smokeFrameCNT == 1)
	{
		trackingSmoke.ProcessKey('r');
	}
	if (smokeFrameCNT > 1)
	{
		pointsSmoke = trackingSmoke.Process(input);
		trackingSmoke.Draw(frameOrg);
		vector<Point2f> currentPoints;
		vector<Point2f> previousPoints;
		//Put Points in seperate vectors
		previousPoints = pointsSmoke[1];
		currentPoints = pointsSmoke[0];
		float maxPoints = currentPoints.size();
		//cout << currentPoints << endl;
		//cout << previousPoints << endl;
		if (smokeFrameCNT > 2)
		{
			//cout << maxPoints << endl;
			float upDirection = 0;
			float deltaY = 0, deltaX = 0;
			for (int m = 0; m < maxPoints; m++)
			{
				deltaY = currentPoints[m].y - previousPoints[m].y;
				deltaX = currentPoints[m].x - previousPoints[m].x;
				//cout << "X\t" << deltaX << endl;
				//cout << "Y\t" << deltaY << endl;
				if (deltaY < 0 && abs(deltaY/deltaX) > 1.5)
				{
					upDirection++;
				}
			}
			//cout << "++++++++++++++++++\t" << maxPoints << endl;
			//cout << 100 * (upDirection / maxPoints) << " %" << endl;
			if ((100 * (upDirection / maxPoints)) > 80.0 && firstStepSmokeDet)
			{
				shotmaybeSmoke = true;
				putText(frameOrg, "SMOKE", Point(50, 30), FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 255, 0), 2);
			}
		}
	}
}

// Start Point of Flame Detection (3....end Block (Thread))
void flameDetection(Mat fT_, Mat fT1_, Mat fT2_, Mat b_, Mat thr_)
{
	//Motion Detection with Dynamic Background for 1st Step in flame detection
	mdVec = motionDetection(fT_, fT1_, fT2_, b_, thr_);
	b = mdVec.MATVEC[1].clone();
	thr = mdVec.MATVEC[2].clone();
	
	if (mdVec.FCNT > 10)
	{
		//Get Determine Color Range for 2nd step in flame Detection
		Mat fT_g, fT1_g, diff_out;
		cvtColor(fT_, fT_g, CV_BGR2GRAY);
		cvtColor(fT2_, fT1_g, CV_BGR2GRAY);
		absdiff(fT_g, fT1_g, diff_out);
		threshold(diff_out, diff_out, 50, 255, CV_THRESH_BINARY);
		Mat flameColorOutput = diff_out & flameColorDet();
		test = flameColorDet();
		//Morphological for eliminate noises (4th Block - Flame)
		Mat tempMorpho, flameMorphOutput;
		dilate(flameColorOutput, tempMorpho, flameOpeningKernel);
		erode(tempMorpho, flameMorphOutput, flameClosingKernel);
		//erode(flameMorphOutput, flameMorphOutput, smokeErodeKernel);
		//morphologyEx(flameColorOutput, tempMorpho, MORPH_OPEN, flameOpeningKernel);
		//morphologyEx(tempMorpho, flameMorphOutput,MORPH_OPEN, flameOpeningKernel);
		
		//Find Components
		flameConnectedComponentsstats(flameMorphOutput);
		
		//Optical Flow
		Mat gray2BGR;
		Mat channel[3];
		vector<Mat> channelOut;
		split(frame, channel);
		channel[0] = channel[0] & flameMorphOutput;
		channel[1] = channel[1] & flameMorphOutput;
		channel[2] = channel[2] & flameMorphOutput;
		channelOut.push_back(channel[0]);
		channelOut.push_back(channel[1]);
		channelOut.push_back(channel[2]);
		merge(channelOut, gray2BGR);
		test = gray2BGR.clone();
		//cvtColor(flameMorphOutput, gray2BGR, CV_GRAY2BGR);
		flameOpticalFlow(gray2BGR);
	}
}


// Start Point of Smoke Detection (3....end Block (Thread))
void smokeDetection(Mat BSforSmoke_, Mat fT_, Mat fT1_, Mat fT2_)
{
	//#^#
	Mat outThr(frame.rows, frame.cols, CV_8UC1);
	//#^#
	threshold(BSforSmoke_, outThr, 50, 255, CV_THRESH_BINARY);

	Mat kernel = Mat::ones(Size(5, 5),CV_8U);
	dilate(outThr, outThr, kernel);
	erode(outThr, outThr, kernel);

	Mat tempMorpho, smokeMorphOutput;
	morphologyEx(smokeColorDet() & outThr, tempMorpho, MORPH_DILATE, smokeDilateKernel);
	morphologyEx(tempMorpho, smokeMorphOutput, MORPH_ERODE, smokeErodeKernel);
	
	Mat absColor;
	absColor = absoluteColorChange(smokeMorphOutput, fT_, fT1_);
	smokeConnectedComponentsstats(absColor);
	test = absColor.clone();
	Mat gray2BGR;
	cvtColor(absColor, gray2BGR, CV_GRAY2BGR);
	smokeOpticalFlow(gray2BGR);
}

int main()
{
	try
	{	
		//Restart after divided by Zero
		signal(SIGFPE, handler);
		
		//Config frame LED
		wiringPiSetup();
		pinMode(frameLED,OUTPUT);
		digitalWrite(frameLED,LOW);
		frameBool = false;
		
		//Start Alarm Thread
		thread report(changemode);
		
		//Select Video Source
		raspicam::RaspiCam_Cv capture;
		capture.set(cv::CAP_PROP_FRAME_WIDTH, 640);
		capture.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
		capture.set(CV_CAP_PROP_FORMAT, CV_8UC3);
		capture.set(CV_CAP_PROP_SATURATION, 50);
		//capture.set(CV_CAP_PROP_BRIGHTNESS, 30);
		
		//For Debug Mode
		//namedWindow("ISTA CO.");
		//moveWindow("ISTA CO.",10,10);
		//VideoCapture cap("sBehindtheFence.avi");
		
		if (!capture.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
		
		//Get FPS of input video and dealy between two frames
		//double rate = capture.get(CV_CAP_PROP_FPS);
		int delay = 100 / 100;

		//Declare some Mat and Variable
		Mat fT, fT1, fT2, staticb, BSforSmoke;

		//Create Base thr Mat
		Mat thr0 = Mat::ones(480 ,640, CV_8UC1);
		thr0 = thr0 * thrFirstFrame;
	
		//Create a window for display results
		int firstFrameCNT = 1;

		//Using MOG2 for Smoke Section
		Ptr<BackgroundSubtractor> pMOG2 = createBackgroundSubtractorMOG2(20, 25, true);


		cerr << "FirstStep Started Correctly\n";
		//Main loop (while have frame in input)
		for (int i=0; i<10000000; i++) {
			capture.grab();
			capture.retrieve (frame);
			
			if (frame.empty())
			{
				cerr << "NOT FOUND INPUT IMAGE\n";
				system("sudo reboot");
			}
			
			//For Debug Mode
			//cap.read(frame);
			
			frameOrg = frame.clone();

			//SB for Smoke Section
			pMOG2->apply(frame, BSforSmoke, 0.01);

			frame = grayWorld(frame, "manual_algorithm");
			
			if (firstFrameCNT > 2)
				fT2 = fT1.clone();
			if (firstFrameCNT > 1)
				fT1 = fT.clone();
			if (firstFrameCNT > 0)
				fT = frame.clone();
			if (firstFrameCNT == 3)
			{
				b = fT.clone();
				mdVec = motionDetection(fT, fT1, fT2, b, thr0);
				staticb = mdVec.MATVEC[1].clone();
				b = mdVec.MATVEC[1].clone();
				thr = mdVec.MATVEC[2].clone();
			}
			if (firstFrameCNT > 3)
			{
				Mat thr0 = Mat::ones(fT.rows, fT.cols, CV_8UC1);
				thr0 = thr0 * thrFirstFrame;
				
				//Trying to use thread for the first time :D
				//thread smokeThread(smokeDetection, BSforSmoke, fT, fT1, fT2);
				thread flameThread(flameDetection, fT, fT1, fT2, b, thr);
				//smokeThread.join();
				flameThread.join();

				//Show results in Display
				//imshow("image", test);
				//imshow("ima_ge", mdVec_[0]);
				//imshow("ISTA CO.", frameOrg);
				
				//Frame LED output
				if (frameBool == false)
				{
					digitalWrite(frameLED,HIGH);
					frameBool = true;
				} else {
					digitalWrite(frameLED,LOW);
					frameBool = false;
				}
				
				imwrite("/home/pi/IS/webserver/DB/frame.jpg", frameOrg);
				
				//Wait as ms between each frame
				waitKey(1);
			}
			if (firstFrameCNT < 80)
			{
				firstFrameCNT++;
			}
			else
			{
				//staticb = fT1.clone();
				firstFrameCNT = 3;
			}
		}
	}
	
	catch(cv::Exception & e)
	{
		cerr << "ERROR Catch\n";
		system("sudo reboot");
	}
	return 0;
}
