"use client"; 

import React, { useState } from "react";
import { Image, Button } from "antd";
import { DownloadOutlined, FullscreenOutlined } from "@ant-design/icons";

export function ImageFromSrc({ imageBase64, name="image", alt = "Image" }: { imageBase64: string; name?: string; alt?: string }) {
    const [hovered, setHovered] = useState(false);
    const [isFullscreen, setIsFullscreen] = useState(false);
    
    const handleDownload = async (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        event.stopPropagation();
    
        try {
            console.log("Downloading:", imageBase64); // Debugging: Check the URL
    
            const response = await fetch(imageBase64);
            console.log("Response", response);
            console.log("Response headers:", response.headers);
    
            const blob = await response.blob();
            console.log("Blob size:", blob.size, "Blob type:", blob.type);
    
            if (blob.size === 0) {
                throw new Error("Downloaded file is empty");
            }
    
            const mimeType = blob.type || "image/png"; // Fallback to PNG
    
            const blobUrl = URL.createObjectURL(new Blob([blob], { type: mimeType }));
    
            const link = document.createElement("a");
            link.href = blobUrl;
            link.download = name; // Force correct file extension
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
    
            URL.revokeObjectURL(blobUrl);
    
        } catch (error) {
            console.error("Error downloading the image:", error);
        }
    };

    const handleFullscreen = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        event.stopPropagation();
        setIsFullscreen(true);
    };

    const handleCloseFullscreen = () => {
        setIsFullscreen(false);
    };
    
  
    return (
      <>
        <div 
          style={{ position: "relative", display: "inline-block" }}
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
        >
          {(hovered || document.activeElement?.classList.contains("download-button")) && (
            <div style={{ position: "absolute", top: 10, left: 10, zIndex: 10, display: "flex", gap: "8px" }}>
              <Button 
                  type="text" 
                  icon={<DownloadOutlined style={{ color: "white" }} />} 
                  onClick={handleDownload} 
                  style={{
                      backgroundColor:"rgba(100, 100, 100, 0.6)",
                      borderRadius: "8px",
                      padding: "8px",
                      cursor: "pointer",
                      boxShadow: "0 4px 4px rgba(0, 0, 0, 0.1)",
                  }}
              />
              <Button 
                  type="text" 
                  icon={<FullscreenOutlined style={{ color: "white" }} />} 
                  onClick={handleFullscreen} 
                  style={{
                      backgroundColor:"rgba(100, 100, 100, 0.6)",
                      borderRadius: "8px",
                      padding: "8px",
                      cursor: "pointer",
                      boxShadow: "0 4px 4px rgba(0, 0, 0, 0.1)",
                  }}
              />
            </div>
          )}
          <Image src={imageBase64} alt={alt} style={{ maxWidth: "100%", height: "auto" }} preview={false} />
        </div>

        {isFullscreen && (
          <div 
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              width: "100vw",
              height: "100vh",
              backgroundColor: "rgba(0, 0, 0, 0.9)",
              zIndex: 9999,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              cursor: "pointer",
              animation: "fadeIn 0.3s ease-in-out"
            }}
            onClick={handleCloseFullscreen}
          >
            <img 
              src={imageBase64} 
              alt={alt} 
              style={{ 
                maxWidth: "90vw", 
                maxHeight: "90vh", 
                objectFit: "contain",
                animation: "zoomIn 0.3s ease-out"
              }} 
            />
          </div>
        )}
      </>
    );
};
  
// export const ImageFromSrcs = ({ imageBase64s }: { imageBase64s: string[] }) => {
//     return (
//       <div>
//         {imageBase64s.map((imageBase64, index) => (
//             <ImageFromSrc key={index} imageBase64={imageBase64} />
//         ))}
//       </div>
//     )
// };

export default function ImageClientWrapper({ images }: { images: any[] }) {
  return (
    <div>
      {images.map((image, index) => (
          <ImageFromSrc key={index} imageBase64={image.download_link} name={image.name.split("/").pop()} alt={image.name.split("/").pop()} />
      ))}
    </div>
  )
}