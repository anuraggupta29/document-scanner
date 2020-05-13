<h1>Document Scanner and OCR</h1>
<h4>In Progress</h4>
 
 <ul>
 <li>This is a desktop based GUI Document Scanner.</li>
 <li>It can scan multiple images at once.</li>
 <li>It automatically detects the 'document' part from the image.</li>
 <li>It corrects its orientation and perspective.</li>
 <li>The GUI will have the feature to manually select the 'document' part from each image, in case there's an error in automatic detection.</li>
 <li>It can save the image in multiple modes and resolution.</li>
 <li>It can also save all the images as a simgle pdf.</li>
 <li>It will also have the feature of optical character recognition.</li>
 </ul>
 
 <h4>How document detection works on each image?</h4>
 
 <ul>
 <li>It resizes a copy of the image for manipulation.</li>
 <li>It then grayscales the image.</li>
 <li>Then it applies a bilateral filter to it (blurs the image while preserving edges).</li>
 <li>It produces a canny image (binary edges only) with the threshold dependent on median of intensity values of image pixels.</li>
 <li>It then detects the contours in the image (the curves). </li>
 <li>Then it takes the largest contour based on perimeter (As the document part will have the largest perimeter.<br>
  <i>Note : The document will also have the largest area but most of the time the contour detected is not a closed curve, because of which its area becomes very small but the perimeter remains large.</i></li>
 <li>Next it takes a convex hull of our selected contour (smallest polygon enclosing the contour).</li>
 <li>Then it uses approximatePolyDP to approximate the convex hull as a rectangle.</li>
 <li>Thus it obtains the 4 corners of our document.</li>
 <li>Then it scales to coordinates according to the original image size.</li>
 <li>From those 4 coordinates we identify which one is the tl, tr, br, bl coordinate.</li>
 <li>The it calculates the height and width of our document portion.</li>
 <li>Then it does a perspective transform of the original image with our rectangle coordinates and produce the transformed image.</li>
 </ul>
 
 <h4>Note : Rest of the features are yet to be added.</h4>
 
 
 
 
