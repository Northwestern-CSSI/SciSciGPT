"use client";

import React, { useState, useEffect } from "react";
import { cn } from '@/lib/utils'
import { defaultExpandedState } from '@/llm.config'

import { ExpandOutlined, CompressOutlined } from "@ant-design/icons";
import '@/lib/chat/components/index.css';

import { Collapse, Button } from "antd";
const { Panel } = Collapse;
import { Markdown } from '@/lib/chat/components/markdown'

interface CollapsibleUIProps {
  children: React.ReactNode;
  header: string | React.ReactNode;
  shouldCollapse?: boolean;
}

const CollapsibleUI: React.FC<CollapsibleUIProps> = ({ children, header, shouldCollapse }) => {
  children = <div className="px-2"><div className="border-l px-4">{children}</div></div>
  
  const isExpanded = shouldCollapse !== undefined ? !shouldCollapse : defaultExpandedState;
  
  return (
    <div className="dark:prose-invert custom-collapse-text">
      <Collapse 
        bordered={false} 
        ghost={true}
        size="middle"
        style={{ width: '100%' }} 
        defaultActiveKey={isExpanded ? ["1"] : []}
        items={[{ 
          key: '1', 
          label: header, 
          children: children,
        }]}
        />
    </div>
  );
};

export default CollapsibleUI;