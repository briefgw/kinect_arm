/*
 * Senior Design 2018 - Hatata & Magnan
 * The George Washington University
 *
 * This API focuses on the algorithms to support our modeling
 * functionality.
 * It relies on a previous Senior Design Project (Karl Presner)
 * for motor execution and communicated with via Python-C++ Socket server
 *
 * This document is broken down into a few sections:
 * (I)    Includes
 * (II)   Constants for calibration and current Environment
 * (III)  Creation of Aruco Markers for printing
 * (IV)   Camera Calibration
 * (V)    Saving Images for testing
 * (VI)   Calibration Analysis
 * (VII)  Importing saved images for analysis
 * (VIII) Obtaining live image for ANALYSIS
 * (IX)   Client for Python-C Server
 * (X)    Actuation
 *
 */

 /* (I) INCLUDES + NAMESPAGES */

 #include "opencv2/core.hpp"
 #include "opencv2/imgcodecs.hpp"
 #include "opencv2/imgproc.hpp"
 #include "opencv2/highgui.hpp"
 #include "opencv2/aruco.hpp"
 #include "opencv2/calib3d.hpp"

 #include <sstream>
 #include <iostream>
 #include <fstream>
 #include <vector>
 #include <math.h>
 #include <string.h>
 #include <sys/socket.h>
 #include <arpa/inet.h>
 #include <netdb.h>
 #include <unistd.h>
 #include <sys/types.h>
 #include <dirent.h>
 #include <errno.h>
 #include <iostream>
 /*
 #include<stdio.h>      //printf
 #include<string.h>     //strlen    // Might need these for the socket communication if not working.
 #include<string>       //string
 */

 using namespace std;
 using namespace cv;
 using std::vector;

 /* (II) CONSTANTS */

 // Constants for Calibration
 const float calibrationSquareDemension = .0239f; //meters
 const float arucoSquareDimension = .160f;   //meters - 160mm = 16cm
 const Size chessboardDimensions = Size(6, 9); //Size of calibration board (given)

 // Runtime Constants
 Mat cameraMatrix = Mat::eye(3, 3, CV_64F);
 Mat distanceCoefficients;
 vector<int> markerIds;
 vector< vector<Point2f> > markerCorners;
 string KinectScan_path = "../../../src/Kinect_code/output/";

 // Known location of markers in Test Environment
 /* TODO: Update these values with those recorded. */
 std::vector<Vec3d> translationVectorsToOrigin;
 Vec3d mk0 (0, -0.4318f, 0);
 Vec3d mk1 ( 0.4318f, 0, 0);
 Vec3d mk2 (0,  0.4318f, 0);
 Vec3d mk3 (-0.4318f, 0, 0);

 // All markers have NOT been rotated with respect to the origin
 Vec3d markerRotation (0, 0, 0);

 // Global variable to determine where the Kinect actually is
 Vec3d kinectActual (0, 0, 0);
 Vec3d kinectRVec   (0, 0, 0);  // In Euler notation NOT rotation Matrix
 Mat kinectRotationMatrix = Mat::eye(3, 3, CV_64F);


 /* (III) CREATION OF ARUCO MARKERS */

 // Only execute on initial installation of API
 void createArucoMarkers() {
   Mat outputMarker;

   //Ptr<aruco::Dictionary> markerDictionary =
   //  aruco::getPredefinedDictionary(aruco::PREDEFINED_DICTIONARY_NAME::DICT_4x4_50);

   Ptr<aruco::Dictionary> markerDictionary =
       aruco::getPredefinedDictionary( 0 );



   for ( int i = 0 ; i < 50 ; i++ ) {
     aruco::drawMarker(markerDictionary, i, 500, outputMarker, 1);
     ostringstream convert;
     string imageName = "4x4Marker_";
     convert << imageName << i << ".jpg";
     imwrite(convert.str(), outputMarker);
   }
 }

 /* (IV) CAMERA CALIBRATION */

 void createKnowBoardPositions(Size boardSize, float squareEdgeLength, vector<Point3f> corners ) {
   for ( int i = 0 ; i < boardSize.height; i++ ) {
     for ( int j = 0 ; j < boardSize.width; j++ ) {
       // Push in all calculated of expected Point3f
       corners.push_back( Point3f(j * squareEdgeLength, i * squareEdgeLength, 0.0f) );
     }
   }
 }

 void getChessboardCorners( vector<Mat> images, vector< vector<Point2f> >& allFoundCorners, bool showResults = false ) {
   for ( vector<Mat>::iterator iter = images.begin(); iter != images.end(); iter++ ) {
     vector<Point2f> pointBuf;
     // Using opencv function
     bool found = findChessboardCorners(*iter, Size(9,6), pointBuf, CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_NORMALIZE_IMAGE );

     if ( found ) {
       allFoundCorners.push_back(pointBuf);
     }

     if ( showResults ) {
       drawChessboardCorners(*iter, Size(9,6), pointBuf, found);
       imshow("Looking for Corners", *iter);
       waitKey(0); //Does not terminate until done
     }
   }
 }

 void cameraCalibration( vector<Mat> calibrationImages, Size boardSize, float squareEdgeLength, Mat& cameraMatrix, Mat& distanceCoefficients ) {
   printf("Enters function successfully\n");
   vector< vector<Point2f> > checkerboardImageSpacePoints;
   getChessboardCorners( calibrationImages, checkerboardImageSpacePoints, false );
   printf("successfully gets chessboardCorners\n");
   // Create known board positions
   vector< vector<Point3f> > worldSpaceCornerPoints(1);

   createKnowBoardPositions(boardSize, squareEdgeLength, worldSpaceCornerPoints[0]);
   worldSpaceCornerPoints.resize(checkerboardImageSpacePoints.size(), worldSpaceCornerPoints[0]);

   vector<Mat> rVectors, tVectors;
   distanceCoefficients = Mat::zeros(8, 1, CV_64F);

   printf("I successfully getChessboardCorners, createKnowBoardPositions, and set distanceCoefficients\n");

   // TODO ISSUE! passing in correct points but not recognizing in opencv function
   cv::calibrateCamera(worldSpaceCornerPoints, checkerboardImageSpacePoints, boardSize, cameraMatrix, distanceCoefficients, rVectors, tVectors);
 }

 bool saveCameraCalibration( string name, Mat cameraMatrix, Mat distanceCoefficients ) {
   printf("ENTERS CAMERA CALIBRATION SUCCESSFULLY\n");

   ofstream outStream;
   outStream.open(name.c_str());

   if ( outStream ) {
     uint16_t rows = cameraMatrix.rows;
     uint16_t columns = cameraMatrix.cols;

     // Push out rows and cols to file << endl = \n
     outStream << rows << endl;
     outStream << columns << endl;

     for ( int r = 0 ; r < rows ; r++  ) {
       for ( int c = 0 ; c < columns ; c++ ) {
         double value = cameraMatrix.at<double>(r, c);
         outStream << value << endl;
       }
     }

     rows = distanceCoefficients.rows;
     columns = distanceCoefficients.cols;

     // Push out rows and cols to file << endl = \n for distanceCoefficients
     outStream << rows << endl;
     outStream << columns << endl;

     for ( int r = 0 ; r < rows ; r++  ) {
       for ( int c = 0 ; c < columns ; c++ ) {
         double value = distanceCoefficients.at<double>(r, c);
         outStream << value << endl;
       }
     }

     outStream.close();
     return true;
   }
   return false;
 }

 // Fully working. Takes in precalculated calibration values of the camera for analysis
 bool loadCameraCalibration( string name, Mat& cameraMatrix, Mat& distanceCoefficients ) {

   // Bring in the file that we are loading information from
   ifstream inStream;
   inStream.open(name.c_str());

   if ( inStream ) {
     uint16_t rows;
     uint16_t columns;

     inStream >> rows;
     inStream >> columns;

     cameraMatrix = Mat( Size(columns, rows), CV_64F );

     for ( int r = 0 ; r < rows ; r++ ) {
       for ( int c = 0 ; c < columns ; c++ ) {
         double temp = 0.0f;
         inStream >> temp;
         cameraMatrix.at<double>(r,c) = temp;
         //cout << cameraMatrix.at<double>(r,c) << "\n";
       }
     }

     // Find distanceCoefficients
     inStream >> rows;
     inStream >> columns;

     distanceCoefficients = Mat::zeros(rows, columns, CV_64F);

     for ( int r = 0 ; r < rows ; r++ ) {
       for ( int c = 0 ; c < columns ; c++ ) {
         double temp = 0.0f;
         inStream >> temp;
         distanceCoefficients.at<double>(r,c) = temp;
         //cout << distanceCoefficients.at<double>(r,c) << "\n";
       }
     }

     inStream.close();
     return true;
   }

   return false;
 }

 // Function that is called upon installation and recalibration
 void cameraCalibrationProcess( Mat& cameraMatrix, Mat& distanceCoefficients ) {
   Mat frame;
   Mat drawToFrame;

   vector<Mat> savedImages;

   vector< vector<Point2f> > markerCorners, rejectedCandidates;

   VideoCapture vid(0);

   if (!vid.isOpened()) { return; }

   int framesPerSecond = 20;

   namedWindow( "Webcam", CV_WINDOW_AUTOSIZE );

   while(true) {
     if (!vid.read(frame)) {
       break;
     }

     vector<Vec2f> foundPoints;
     bool found = false;

     found = findChessboardCorners( frame, chessboardDimensions, foundPoints, CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_NORMALIZE_IMAGE );
     frame.copyTo( drawToFrame );
     drawChessboardCorners(drawToFrame, chessboardDimensions, foundPoints, found);
     if (found) {
       imshow("Webcam", drawToFrame);
     } else {
       imshow("Webcam", frame);
     }
     char character = waitKey(1000/framesPerSecond);

     switch (character) {
       case ' ':
         printf("SPACE: Looking for image\n");
         // Saving image
         if (found) {
           printf("Image found\n");
           Mat temp;
           frame.copyTo(temp);
           savedImages.push_back(temp);
         }
         break;
       case 'f':
         // Enter Key - start calibration
         // First check that we have enough
         printf("ENTER: Save File\n");
         printf("COUNT Image found: %i\n", savedImages.size());
         if ( savedImages.size() > 15 ) {
           // TODO: Issue with this call in my method to other method
           printf("Enters. Correct number of images found\n");
           cameraCalibration(savedImages, chessboardDimensions, calibrationSquareDemension, cameraMatrix, distanceCoefficients);
           printf("Calibration Complete...Waiting to save file\n");
           saveCameraCalibration("ILoveCameraCalibration", cameraMatrix, distanceCoefficients);
           printf("SUCCESSFULLY saved calibration\n");
         }
         printf("Not enough images found\n");
         break;
       case 27:
         // ESC Key
         return;
         break;

     }
   }
 }

 /* (V) SAVING IMAGES */
 // Currently in it's own function save_photos.cpp with build of ./save [image_name.png]

 /* (VI) CALIBRATION ANALYSIS */
 int analyzeFrame( vector< vector<Point2f> > markerCorners, vector<Vec3d> rotationVectors, vector<Vec3d> translationVectors, vector<int> markerIds ) {

   printf("\nLocation of Kinect for found markers...\n");
   // Print out rotationVectors and translationVectors for found Markers
   for ( int r = 0 ; r < rotationVectors.size() ; r++ ) {
     printf("\tMarkerId: %d\n", markerIds[r]);
     cout << "\t[r,p,y] " << rotationVectors.at(r)[0] <<", " << rotationVectors.at(r)[1] <<", " << rotationVectors.at(r)[2] << endl;
     cout << "\t[x,y,z] " << translationVectors.at(r)[0] <<", " << translationVectors.at(r)[1] <<", " << translationVectors.at(r)[2] << endl;
     printf("\n");
   }

  //  printf("Stored values for markers...\n");
  //  for ( int r = 0 ; r < translationVectorsToOrigin.size() ; r++ ) {
  //    printf("MarkerId: %d\n", r);
  //    cout << "[x,y,z] " << translationVectorsToOrigin.at(r)[0] <<", " << translationVectorsToOrigin.at(r)[1] <<", " << translationVectorsToOrigin.at(r)[2] << endl;
  //    printf("\n");
  //  }

   Mat tempMat3x3 = Mat::eye(3, 3, CV_64F);

   /* TODO: Find average rotation

   // Add values for each marker to kinectRotationMatrix;
   for ( int i = 0 ; i < rotationVectors.size() ; i++ ) {
     printf("Gets here\n");
     Rodrigues(rotationVectors[i], tempMat3x3);
     //transpose(tempMat3x3, tempMat3x3Inverse);
     for ( int j = 0 ; j < 3 ; j++ ) {
       for ( int k = 0 ; k < 3 ; k++ ) {
         //const double* Mi = kinectRotationMatrix.ptr<double>(i);
         kinectRotationMatrix.at<double>(j,k) = kinectRotationMatrix.at<double>(j,k) + tempMat3x3.at<double>(j,k);
       }
     }
   }

   // Get Average of final rotation
   // divide all values in kinectRotationMatrix by rotationVectors.size()
   for ( int i = 0 ; i < 3 ; i++ ) {
     for ( int j = 0 ; j < 3 ; j++ ) {
       //const double* Mi = kinectRotationMatrix.ptr<double>(i);
       kinectRotationMatrix.at<double>(i,j) = kinectRotationMatrix.at<double>(i,j) / rotationVectors.size();
     }
   }
   */

   Rodrigues(rotationVectors[0], kinectRotationMatrix); // TODO: Remove when average found
   Rodrigues(kinectRotationMatrix, kinectRVec);

   // TODO Print out Final Rotation

   // translationVectors have the marker coordinates system transformed to the kinect
   // Add each known location to translationVectors
   for ( int t = 0 ; t < translationVectors.size() ; t++ ) {
     int currentMarker = markerIds[t];
     translationVectorsToOrigin.at(currentMarker)[0];
     translationVectors.at(t)[0] = translationVectors.at(t)[0] + translationVectorsToOrigin.at(currentMarker)[0];
     translationVectors.at(t)[1] = translationVectors.at(t)[1] + translationVectorsToOrigin.at(currentMarker)[1];
     translationVectors.at(t)[2] = translationVectors.at(t)[2] + translationVectorsToOrigin.at(currentMarker)[2];

     // Add to kinectActual in the process
     kinectActual[0] += translationVectors.at(t)[0];
     kinectActual[1] += translationVectors.at(t)[1];
     kinectActual[2] += translationVectors.at(t)[2];
   }

    printf("Determining location of Kinect...\nUnaveraged locations determined...\n");
    // Print out updated translationVectors for found Markers adding in known location
    for ( int r = 0 ; r < rotationVectors.size() ; r++ ) {
      printf("\tUsing MarkerId: %d...\n", markerIds[r]);
      cout << "\t[x,y,z] " << translationVectors.at(r)[0] <<", " << translationVectors.at(r)[1] <<", " << translationVectors.at(r)[2] << endl;
      printf("\n");
    }

    // Find average of translationVectors
    // Sum of values in all translationVectors done above
    kinectActual[0] = kinectActual[0] / translationVectors.size();
    kinectActual[1] = kinectActual[1] / translationVectors.size();
    kinectActual[2] = kinectActual[2] / translationVectors.size();

    // Print out results
    printf("Actual location of the camera wrt origin\n");
    cout << "\t[r,p,y] " << kinectRVec[0] <<", " << kinectRVec[1] <<", " << kinectRVec[2] << endl;
    cout << "\t[x,y,z] " << kinectActual[0] <<", " << kinectActual[1] <<", " << kinectActual[2] << endl;
    printf("\n");

    //Print out kinectActual to ensure correct

   return 1;
 }

 /* (VII) IMPORTING SAVED IMAGE FOR ANALYSIS */
 int obtainSavedImage( string name, const Mat& cameraMatrix, const Mat& distanceCoefficients, bool showWindow) {

   // Bring in the file that we are loading image from
   ifstream inStream;
   inStream.open(name.c_str());

   Mat frame;  //Hold frame of info from image

   vector<int> markerIds;
   vector< vector<Point2f> > markerCorners, rejectedCandidates;

   // Aruco part
   aruco::DetectorParameters parameters;

   Ptr<aruco::Dictionary> markerDictionary =
       aruco::getPredefinedDictionary( 0 );

   // Opening Image
   //string projectPath = "/home/tjmagnan/sd-18-hatata_magnan/calibration_actuation";
   string projectPath = "../../../collected_data/";
   string fullPath = projectPath + name.c_str();
   fullPath = name.c_str();
   printf("Attempting to open %s\n%s\n", name.c_str(), fullPath);
   try {
     frame = imread(fullPath);
     // frame = imread(name.c_str());
   }
   catch (runtime_error& ex) {
       fprintf(stderr, "Exception importing image: %s\n", ex.what());
       return 1;
   }
   printf("Image successfully opens!\n");

   if (showWindow) {
     printf("Opening window ...\n");
     namedWindow(name.c_str(), CV_WINDOW_AUTOSIZE);  //Makes the GUI
     printf("Successfully built Window\n");
   }

   vector<Vec3d> rotationVectors, translationVectors;
   printf("Successfully created rotationVectors and translationVectors...\n");

   // Finds them
   aruco::detectMarkers(frame, markerDictionary, markerCorners, markerIds);

   // Outline the markers and label with ids
   if ( showWindow ) { aruco::drawDetectedMarkers(frame, markerCorners, markerIds); }

   // Estimate pose
   aruco::estimatePoseSingleMarkers(markerCorners, arucoSquareDimension, cameraMatrix, distanceCoefficients, rotationVectors, translationVectors );

   // Continually draw the axis
   if ( showWindow ) {
     for ( int i = 0 ; i < markerIds.size() ; i++ ) {
       aruco::drawAxis(frame, cameraMatrix, distanceCoefficients, rotationVectors[i], translationVectors[i], 0.1f);
       // printf("Marker %i found\n", markerIds[i] ); // Only print once but already shown visually
     }
     imshow(name.c_str(), frame);
   }

   if ( showWindow ) {
     while(true) {
      imshow(name.c_str(), frame);

       char character;
       if ( character = waitKey(30) >= 0) break;

       // Once a good photo has been taken
       // press SPACE to exit for analysis
       if ( character == ' ' ) { break; }
     }
   }

   // Perform analysis and determine actual location
   printf("Desired image aquired and markers found. Continuing to analyse image...\n");
   analyzeFrame( markerCorners, rotationVectors, translationVectors, markerIds );

   return 1;
 }

 /* (VIII) OBTAINING LIVE IMAGE FOR ANALYSIS */
 int obtainLiveImage( const Mat& cameraMatrix, const Mat& distanceCoefficients, bool showMarkers) {

   Mat frame;  //Hold frame of info from webcam

   vector<int> markerIds;
   vector< vector<Point2f> > markerCorners, rejectedCandidates;

   // Aruco part
   aruco::DetectorParameters parameters;

   Ptr<aruco::Dictionary> markerDictionary =
       aruco::getPredefinedDictionary( 0 );

   // Use for Kinect
   printf("Initiating VideoCapture\n");
   VideoCapture vid( CAP_OPENNI );
   //VideoCapture vid(CAP_OPENNI_GRAY_IMAGE);

   if ( !vid.isOpened() ) {
     printf("Video fails to open\n");
     return -1;
   }

   printf("Video successfully open!\n");
   printf("Opening window ...\n");

   namedWindow("Webcam", CV_WINDOW_AUTOSIZE);  //Makes the GUI

   printf("Successfully built Window\n");


   vector<Vec3d> rotationVectors, translationVectors;
   printf("Successfully created rotationVectors and translationVectors...\n");

   //while (true) {}

   while(true) {
     if (!vid.read(frame)) {
     //if (!vid.retrieve(frame, CAP_OPENNI_BGR_IMAGE)) {
       printf("Unable to read current frame. Exiting\n");
       return -1;
     }

     // Alters image type
     vid.retrieve(frame, CAP_OPENNI_BGR_IMAGE);

     // Finds them
     aruco::detectMarkers(frame, markerDictionary, markerCorners, markerIds);

     // Outline the markers and label with ids
     if (showMarkers) { aruco::drawDetectedMarkers(frame, markerCorners, markerIds); }

     // Estimate pose
     aruco::estimatePoseSingleMarkers(markerCorners, arucoSquareDimension, cameraMatrix, distanceCoefficients, rotationVectors, translationVectors );

     // Continually draw the axis
     if ( showMarkers ) {
       for ( int i = 0 ; i < markerIds.size() ; i++ ) {
         aruco::drawAxis(frame, cameraMatrix, distanceCoefficients, rotationVectors[i], translationVectors[i], 0.1f);
         // printf("Marker %i found\n", markerIds[i] ); // Only print once but already shown visually
       }
       imshow("Webcam", frame);
     }

     char character;
     if ( character = waitKey(30) >= 0) break;

     // Once a good photo has been taken
     // press SPACE to exit for analysis
     if ( character == ' ' ) { break; }

   }
   // Perform analysis and determine actual location
   printf("Desired frame aquired. Continuing to analyse frame...\n");
   analyzeFrame( markerCorners, rotationVectors, translationVectors, markerIds );

   return 1;
 }

 /* (IX) CLIENT FOR Python-C */

 // Source: http://www.binarytides.com/code-a-simple-socket-client-class-in-c/

 /**
     TCP Client class
 */
 class tcp_client
 {
 private:
     int sock;
     std::string address;
     int port;
     struct sockaddr_in server;

 public:
     tcp_client();
     bool conn(string, int);
     bool send_data(string data);
     string receive(int);
 };

 tcp_client::tcp_client()
 {
     sock = -1;
     port = 0;
     address = "";
 }

 /**
     Connect to a host on a certain port number
 */
 bool tcp_client::conn(string address , int port)
 {
     //create socket if it is not already created
     if(sock == -1)
     {
         //Create socket
         sock = socket(AF_INET , SOCK_STREAM , 0);
         if (sock == -1)
         {
             perror("Could not create socket");
         }

         cout<<"Socket created...\n";
     }
     else    {   /* OK , nothing */  }

     //setup address structure
     if(inet_addr(address.c_str()) == -1)
     {
         struct hostent *he;
         struct in_addr **addr_list;

         //resolve the hostname, its not an ip address
         if ( (he = gethostbyname( address.c_str() ) ) == NULL)
         {
             //gethostbyname failed
             herror("gethostbyname");
             cout<<"Failed to resolve hostname\n";

             return false;
         }

         //Cast the h_addr_list to in_addr , since h_addr_list also has the ip address in long format only
         addr_list = (struct in_addr **) he->h_addr_list;

         for(int i = 0; addr_list[i] != NULL; i++)
         {
             //strcpy(ip , inet_ntoa(*addr_list[i]) );
             server.sin_addr = *addr_list[i];

             cout<<address<<" resolved to "<<inet_ntoa(*addr_list[i])<<endl;

             break;
         }
     }

     //plain ip address
     else
     {
         server.sin_addr.s_addr = inet_addr( address.c_str() );
     }

     server.sin_family = AF_INET;
     server.sin_port = htons( port );

     //Connect to remote server
     if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
     {
         perror("connect failed. Error");
         return 1;
     }

     cout<<"Connected to server...\n";
     return true;
 }

 /**
     Send data to the connected host
 */
 bool tcp_client::send_data(string data)
 {
     //Send some data
     if( send(sock , data.c_str() , strlen( data.c_str() ) , 0) < 0)
     {
         perror("Send failed : ");
         return false;
     }
     cout<<"Data sent successfully...\n";

     return true;
 }

 /**
     Receive data from the connected host
 */
 string tcp_client::receive(int size=512)
 {
     char buffer[size];
     string reply;

     //Receive a reply from the server
     if( recv(sock , buffer , sizeof(buffer) , 0) < 0)
     {
         puts("Unable to recieve response from server...");
     }

     reply = buffer;
     return reply;
 }

 // Communication with Karl's python code
 int socket_request(string data) {
   cout<<"Initiating socket for motor movement...";

   tcp_client c;

   // Connect to host
   c.conn("localhost", 5000);

   // Sending data
   c.send_data(data);

   // Recieve and echo reply data
   cout<<"Server response: ";
   cout<<c.receive(1024);
   cout<<"\n";

   // Motors have been moved
   return 0;
 }

 /* (X) ACTUATION */

 // Write camera intrinsics to file for Tarek to pull
 bool write_intrisics( string name ) {

   // TODO: Call script to cd to file with images

   ofstream outStream;
   outStream.open(name.c_str());

   if ( outStream ) {
     // tVector
     outStream << "TVector" << endl;
     outStream << kinectActual[0] << endl;
     outStream << kinectActual[1] << endl;
     outStream << kinectActual[2] << endl << endl;

     // rVector
     uint16_t rows = kinectRotationMatrix.rows;
     uint16_t columns = kinectRotationMatrix.cols;

     for ( int r = 0 ; r < rows ; r++  ) {
       for ( int c = 0 ; c < columns ; c++ ) {
         double value = kinectRotationMatrix.at<double>(r, c);
         outStream << value << "\t";
       }
       outStream << endl;
     }

     outStream << endl;

     // Camera intrinsics
     outStream << "Camera Intrinsics: focal height width" << endl;
     outStream << "575.816 480 640" << endl;


     outStream.close();

     //TODO: Call script to move file change directories back
     return true;
   }
   return false;

 }

 // Conversion functions
 Vec3d cartesian_to_polar( Vec3d cartesian ) {
   double r, theta = 0;
   r = sqrt( cartesian[0]*cartesian[0] + cartesian[1]*cartesian[1] );
   theta = atan( cartesian[1]/cartesian[0] );
   Vec3d polar ( r, theta, cartesian[2] );

   return polar;
 }

 Vec3d polar_to_cartesian( Vec3d polar ) {
   double x, y = 0;
   x = polar[0] * cos( polar[1] );
   y = polar[0] * sin( polar[1] );
   Vec3d cartesian ( x, y, cartesian[2] );
   return cartesian;
 }

 bool validLocation( Vec3d originalPolar ) {

   // TODO: Save values as constants above

   // format r, theta, z
   double theta = originalPolar[1];
   double r = originalPolar[r];

   // Ensure theta is valid TODO: Correct max angle
   if ( theta < 0 || theta > 330 ) { return false; }

   // Ensure r is valid
   if ( r < .1 ) { return false; }

   // Alter (r, theta, z)

   // else if (  ) {  }

   else {
     return true;
   }

 }

 // Basic functions when location isn't specified

 int down() {
   // open one x2 close the other
 }

 int up() {
   // open one x2 close the other - inverse
 }

 int left() {
   // Stepper motor
   socket_request("move(3, 10)");
 }

 int right() {
   // stepper motor
 }

 int rotateCamera() {
   // open one x2 close the other
 }

 // Error correct
 int error_correct( Vec3d desired_endpoint ) {
     //TODO: Get actual location of camera (actual_pt)
         //TODO: Call upon Arucu & opencv libraries
     //TODO: Margin of error mesuring
     //TODO: If within, simply return | else continue
     //TODO: Not within error, call move function between points
     //TODO: move( actual_pt, desired_endpoint )
 }

 //

 // Move to location
 // Takes in cartesian coordinates
 int move( Vec3d old_pt_cart, Vec3d new_pt_cart ) {
     // Find polar coordinates for analysis
     Vec3d new_pt, old_pt;

     //TODO: Get differences in theta and move stepper motor
     double theta_diff = new_pt[1] - old_pt[1];

     //TODO: Get differences in r(radius)
     double r_diff = new_pt[0] - old_pt[0];

     //TODO: Get differences in z
     double z_diff = new_pt[2] - old_pt[2];

     //TODO: Determine what the z_diff translates to in stepper movements

     //TODO: Determine the combination of movements of other motors to get to correct r & z
         // Longer term

     //TODO: Ensure that moves are valid, if not change to valid, or throw error (return -1;)
      // Within min and maximum of Motor movements

     //TODO: Iniate Socket communication and Call Karl's API to move points
        // Stepper motor for z
        // Continued

     //TODO: Call calibration function
     error_correct( new_pt );
     return 1;
 }

 // When running using KinectScan.cpp rather than obtaining live images they are already happing in the background
 // This function returns the name of the pcl and jpg images to analyze
 string obtainMostRecentImage() {
   string image = "";
   // Directory path of saved images is saved globally as KinectScan_path

   // List of all images in the folder
   vector<string> files;
   string dir = KinectScan_path;              //Not currently in use
   dir = "../testing/winter_break_photos/";

   // Alternative
   system("./getImage.sh");   // Find the image

   // Load image name from text file
   ifstream inFile;

   inFile.open("../build/mostRecent.txt");

   if (!inFile) {
      cout << "Unable to open file";
      exit(1); // terminate with error
   }

   getline(inFile, image);

   inFile.close();

   // Get substring without extention
   image = image.substr( 0, image.length() - 4 );
   //image = image.substr( 0, image.find(".") );
   cout << "Most recent image taken: " << image << endl;

   return image;
 }

 // Public API
 // Takes in a desired endpoint, determines the current location and returns the string of the name of the image from that pose (jpg and pcl)
 // user can manually pull kinectActual from global after running new_pose()
 string new_pose( Vec3d desired_endpoint_cart ) {

   // Find most recent image
   string mostRecentImage = obtainMostRecentImage();

   // Must concatinate extention for obtainSavedImage
   mostRecentImage = mostRecentImage + ".png";

   // Analyze mostRecentImage
   obtainSavedImage(mostRecentImage, cameraMatrix, distanceCoefficients, true);

   //Current location saved globally
   move(kinectActual, desired_endpoint_cart);

   // Recursively error correct until margin of error
   error_correct(desired_endpoint_cart);

   // Obtain mostRecentImage again; Updated with current location
   mostRecentImage = obtainMostRecentImage();

   //TODO: Get .txt file information that GUI needs for analysis

   // Return image name to user to load
   return mostRecentImage;
 }

 //Initial calls within any running instance
 void load(int argc, char** argv) {
   // Add elements to translationVectorsToOrigin vector
   translationVectorsToOrigin.push_back(mk0);
   translationVectorsToOrigin.push_back(mk1);
   translationVectorsToOrigin.push_back(mk2);
   translationVectorsToOrigin.push_back(mk3);

   loadCameraCalibration("KinectCalibration", cameraMatrix, distanceCoefficients);
 }
