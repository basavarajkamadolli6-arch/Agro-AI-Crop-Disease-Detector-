import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';


void main() {
  runApp(const AgroAIApp());
}


// --------------------------------------------------
// MAIN APPLICATION
// --------------------------------------------------

class AgroAIApp extends StatelessWidget {
  const AgroAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AgroAI',
      debugShowCheckedModeBanner: false,

      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
        ),

        useMaterial3: true,
      ),

      home: const HomePage(),
    );
  }
}


// --------------------------------------------------
// HOME PAGE
// --------------------------------------------------

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}


class _HomePageState extends State<HomePage> {

  File? selectedImage;

  bool isLoading = false;

  String? diseaseName;

  double? confidence;

  String? errorMessage;


  final ImagePicker imagePicker = ImagePicker();


  // ------------------------------------------------
  // SELECT IMAGE FROM GALLERY
  // ------------------------------------------------

  Future<void> selectImage() async {

    try {

      final XFile? image =
          await imagePicker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
      );

      if (image == null) {
        return;
      }

      setState(() {

        selectedImage = File(image.path);

        diseaseName = null;

        confidence = null;

        errorMessage = null;

      });

    } catch (error) {

      setState(() {

        errorMessage =
            'Unable to select the image.';

      });

    }
  }


  // ------------------------------------------------
  // CAPTURE IMAGE USING CAMERA
  // ------------------------------------------------

  Future<void> captureImage() async {

    try {

      final XFile? image =
          await imagePicker.pickImage(
        source: ImageSource.camera,
        imageQuality: 85,
      );

      if (image == null) {
        return;
      }

      setState(() {

        selectedImage = File(image.path);

        diseaseName = null;

        confidence = null;

        errorMessage = null;

      });

    } catch (error) {

      setState(() {

        errorMessage =
            'Unable to capture the image.';

      });

    }
  }


  // ------------------------------------------------
  // CONNECT TO DJANGO BACKEND
  // ------------------------------------------------

  Future<void> detectDisease() async {

    if (selectedImage == null) {

      setState(() {

        errorMessage =
            'Please select a plant-leaf image first.';

      });

      return;
    }

    setState(() {

      isLoading = true;

      diseaseName = null;

      confidence = null;

      errorMessage = null;

    });


    try {

      // Android emulator:
      // 10.0.2.2 points to the development computer.
      //
      // Physical phone:
      // Replace this with your computer's LAN IP.
      //
      // Example:
      // http://192.168.1.5:8000/api/predict/

      final Uri apiUrl = Uri.parse(
        'http://10.0.2.2:8000/api/predict/',
      );


      final request = http.MultipartRequest(
        'POST',
        apiUrl,
      );


      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          selectedImage!.path,
        ),
      );


      final streamedResponse =
          await request.send().timeout(
        const Duration(seconds: 120),
      );


      final response =
          await http.Response.fromStream(
        streamedResponse,
      );


      final Map<String, dynamic> data =
          jsonDecode(response.body);


      if (response.statusCode == 200 &&
          data['status'] == 'success') {

        setState(() {

          diseaseName =
              data['plant_disease']?.toString();

          confidence =
              (data['confidence'] as num?)
                  ?.toDouble();

        });

      } else if (response.statusCode == 200 &&
          data['status'] == 'uncertain') {

        setState(() {

          diseaseName =
              data['predicted_class']?.toString();

          confidence =
              (data['confidence'] as num?)
                  ?.toDouble();

          errorMessage =
              data['message']?.toString() ??
              'The prediction is uncertain.';

        });

      } else {

        setState(() {

          errorMessage =
              data['error']?.toString() ??
              'Prediction failed.';

        });

      }

    } catch (error) {

      setState(() {

        errorMessage =
            'Unable to connect to the server. '
            'Check the backend and network.';

      });

    } finally {

      if (mounted) {

        setState(() {

          isLoading = false;

        });

      }

    }
  }


  // ------------------------------------------------
  // USER INTERFACE
  // ------------------------------------------------

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(

        title: const Text(
          'AgroAI 🌱',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),

        backgroundColor: Colors.green,

        foregroundColor: Colors.white,

      ),


      body: SafeArea(

        child: SingleChildScrollView(

          padding: const EdgeInsets.all(20),

          child: Column(

            crossAxisAlignment:
                CrossAxisAlignment.stretch,

            children: [

              const SizedBox(height: 10),


              const Icon(
                Icons.eco,
                size: 75,
                color: Colors.green,
              ),


              const SizedBox(height: 15),


              const Text(
                'Plant Disease Detection',
                textAlign: TextAlign.center,

                style: TextStyle(
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
              ),


              const SizedBox(height: 10),


              const Text(
                'Upload a plant-leaf image '
                'to check for possible diseases.',

                textAlign: TextAlign.center,

                style: TextStyle(
                  fontSize: 16,
                ),
              ),


              const SizedBox(height: 25),


              // IMAGE PREVIEW

              Container(

                height: 260,

                decoration: BoxDecoration(

                  color: Colors.green.shade50,

                  borderRadius:
                      BorderRadius.circular(18),

                  border: Border.all(
                    color: Colors.green.shade200,
                  ),

                ),

                child: selectedImage == null

                    ? const Column(

                        mainAxisAlignment:
                            MainAxisAlignment.center,

                        children: [

                          Icon(
                            Icons.add_a_photo,
                            size: 65,
                            color: Colors.green,
                          ),

                          SizedBox(height: 12),

                          Text(
                            'No image selected',
                            style: TextStyle(
                              fontSize: 17,
                            ),
                          ),

                        ],

                      )

                    : ClipRRect(

                        borderRadius:
                            BorderRadius.circular(18),

                        child: Image.file(

                          selectedImage!,

                          fit: BoxFit.contain,

                          errorBuilder: (
                            context,
                            error,
                            stackTrace,
                          ) {

                            return const Center(
                              child: Text(
                                'Unable to display image.',
                              ),
                            );

                          },

                        ),

                      ),

              ),


              const SizedBox(height: 20),


              // SELECT IMAGE

              OutlinedButton.icon(

                onPressed: isLoading
                    ? null
                    : selectImage,

                icon: const Icon(
                  Icons.photo_library,
                ),

                label: const Text(
                  'Choose from Gallery',
                ),

                style: OutlinedButton.styleFrom(
                  padding:
                      const EdgeInsets.all(15),
                ),

              ),


              const SizedBox(height: 10),


              // CAPTURE IMAGE

              OutlinedButton.icon(

                onPressed: isLoading
                    ? null
                    : captureImage,

                icon: const Icon(
                  Icons.camera_alt,
                ),

                label: const Text(
                  'Take a Photo',
                ),

                style: OutlinedButton.styleFrom(
                  padding:
                      const EdgeInsets.all(15),
                ),

              ),


              const SizedBox(height: 15),


              // DETECT DISEASE

              FilledButton.icon(

                onPressed: isLoading
                    ? null
                    : detectDisease,

                icon: const Icon(
                  Icons.search,
                ),

                label: Text(
                  isLoading
                      ? 'Analyzing...'
                      : 'Detect Disease',
                ),

                style: FilledButton.styleFrom(

                  backgroundColor: Colors.green,

                  padding:
                      const EdgeInsets.all(17),

                ),

              ),


              if (isLoading) ...[

                const SizedBox(height: 20),

                const Center(
                  child: CircularProgressIndicator(),
                ),

                const SizedBox(height: 10),

                const Text(
                  'Please wait while AI '
                  'analyzes the image.',

                  textAlign: TextAlign.center,

                ),

              ],


              // ERROR MESSAGE

              if (errorMessage != null) ...[

                const SizedBox(height: 20),

                Container(

                  padding:
                      const EdgeInsets.all(15),

                  decoration: BoxDecoration(

                    color: Colors.orange.shade50,

                    borderRadius:
                        BorderRadius.circular(12),

                  ),

                  child: Text(

                    errorMessage!,

                    style: const TextStyle(
                      color: Colors.deepOrange,
                    ),

                  ),

                ),

              ],


              // RESULT

              if (diseaseName != null) ...[

                const SizedBox(height: 25),


                Container(

                  padding:
                      const EdgeInsets.all(20),

                  decoration: BoxDecoration(

                    color: Colors.green.shade50,

                    borderRadius:
                        BorderRadius.circular(16),

                    border: Border.all(
                      color: Colors.green.shade200,
                    ),

                  ),

                  child: Column(

                    crossAxisAlignment:
                        CrossAxisAlignment.start,

                    children: [

                      const Text(

                        'Detection Result',

                        style: TextStyle(

                          fontSize: 22,

                          fontWeight:
                              FontWeight.bold,

                        ),

                      ),


                      const SizedBox(height: 15),


                      const Text(
                        'Predicted class:',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                      ),


                      const SizedBox(height: 5),


                      Text(
                        diseaseName!,
                        style: const TextStyle(
                          fontSize: 18,
                        ),
                      ),


                      const SizedBox(height: 15),


                      if (confidence != null) ...[

                        const Text(
                          'Model confidence:',
                          style: TextStyle(
                            fontWeight:
                                FontWeight.bold,
                          ),
                        ),


                        const SizedBox(height: 5),


                        Text(
                          '${confidence!.toStringAsFixed(2)}%',
                          style: const TextStyle(
                            fontSize: 20,
                            color: Colors.green,
                            fontWeight:
                                FontWeight.bold,
                          ),
                        ),

                      ],


                      const SizedBox(height: 15),


                      const Text(

                        'This is an AI prediction, '
                        'not a confirmed diagnosis. '
                        'Seek expert advice before '
                        'applying treatment.',

                        style: TextStyle(
                          fontSize: 13,
                        ),

                      ),

                    ],

                  ),

                ),

              ],


              const SizedBox(height: 30),

            ],

          ),

        ),

      ),

    );

  }

}