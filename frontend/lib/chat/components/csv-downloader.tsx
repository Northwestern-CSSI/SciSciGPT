"use client"; 

import React, { useState } from "react";
import { Button } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import '@/lib/chat/components/index.css'

type CSVDownLoaderProps = {
    src: string; name?: string 
}

const CSVDownLoader = ({ src, name = 'file' }: CSVDownLoaderProps) => {
    
    const handleDownload = async (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        event.stopPropagation();

        try {
            const fileUrl = src; // Change this to actual file URL
    
            const response = await fetch(fileUrl);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    
            const blob = await response.blob();
            const blobUrl = URL.createObjectURL(blob);
    
            const link = document.createElement("a");
            link.href = blobUrl;
            link.download = name;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
        } catch (error) {
            console.error("Error downloading the file:", error);
        }
    };
    
  
    return (
        <div style={{ margin: "16px 0", textAlign: "left" }}>
            <Button
                className="download-btn"
                icon={
                    <div
                        className="download-btn-icon"
                    >
                        <DownloadOutlined />
                    </div>
                }
                size="large"
                onClick={handleDownload}
            >
                <div>
                    <div 
                        style={{
                            // fontWeight: 'bold',
                            textAlign: 'left',
                            marginBottom: '-5px'
                        }}
                    >
                        {name}
                    </div>
                    <span
                        style={{
                            color: "#666",
                            textAlign: 'left',
                            fontSize: 'small'
                        }}
                    >
                        Spreadsheet
                    </span>
                </div>
            </Button>
      </div>
    );
};

export default function CSVDownLoadClientWrapper(props: CSVDownLoaderProps) {
    return <CSVDownLoader {...props} />;
}