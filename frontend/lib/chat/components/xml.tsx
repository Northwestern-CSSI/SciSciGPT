export function completeUnclosedXmlTags(text: string): string {
  const openTags: string[] = [];
  const result: string[] = [];
  let currentIndex = 0;
  
  // Regex to match opening and closing tags
  const tagRegex = /<\/?(\w+)(?:\s[^>]*)?>/g;
  let match;
  
  while ((match = tagRegex.exec(text)) !== null) {
    const fullMatch = match[0];
    const tagName = match[1];
    const isClosingTag = fullMatch.startsWith('</');
    
    // Add text before this tag
    result.push(text.slice(currentIndex, match.index));
    
    if (isClosingTag) {
      // Remove the corresponding opening tag from the stack
      const lastOpenIndex = openTags.lastIndexOf(tagName);
      if (lastOpenIndex !== -1) {
        openTags.splice(lastOpenIndex, 1);
      }
    } else {
      // Check if it's a self-closing tag (ends with />)
      if (!fullMatch.endsWith('/>')) {
        openTags.push(tagName);
      }
    }
    
    // Add the current tag
    result.push(fullMatch);
    currentIndex = match.index + fullMatch.length;
  }
  
  // Add remaining text
  result.push(text.slice(currentIndex));
  
  // Close any remaining open tags in reverse order
  for (let i = openTags.length - 1; i >= 0; i--) {
    result.push(`</${openTags[i]}>`);
  }
  
  return result.join('');
}


export function removeUnpairedBackslashXmlTags(text: string): string {
  const openTags: string[] = [];
  const result: string[] = [];
  let currentIndex = 0;
  
  // Regex to match opening and closing tags
  const tagRegex = /<\/?(\w+)(?:\s[^>]*)?>/g;
  let match;
  
  while ((match = tagRegex.exec(text)) !== null) {
    const fullMatch = match[0];
    const tagName = match[1];
    const isClosingTag = fullMatch.startsWith('</');
    
    // Add text before this tag
    result.push(text.slice(currentIndex, match.index));
    
    if (isClosingTag) {
      // Only add closing tag if there's a corresponding opening tag
      const lastOpenIndex = openTags.lastIndexOf(tagName);
      if (lastOpenIndex !== -1) {
        openTags.splice(lastOpenIndex, 1);
        result.push(fullMatch);
      }
      // If no corresponding opening tag, skip this closing tag
    } else {
      // Check if it's a self-closing tag (ends with />)
      if (!fullMatch.endsWith('/>')) {
        openTags.push(tagName);
      }
      result.push(fullMatch);
    }
    
    currentIndex = match.index + fullMatch.length;
  }
  
  // Add remaining text
  result.push(text.slice(currentIndex));
  
  return result.join('');
}

export function remove_string(text: string, substring: string): string {
  return text.replace(new RegExp(`${substring}`, 'gs'), '');
}

export function process_xml(text: string): string {
  const foldContent = ['thinking', 'think', 'reflection', "search"];
  const foldContentMapping: Record<string, string> = {
    'thinking': 'Thought',
    'think': 'Thought',
    'reflection': 'Reflection',
    'search': 'Search'
  };

	const removeContent = ['count']; // remove count, reward tag
  const boldContent = ['reward', 'step', 'answer', 'observation', 'caption', 'evaluation', 'category', 'report'];

  let processedText = text ? text.trim() : ''
  processedText = completeUnclosedXmlTags(processedText)

  removeContent.forEach(tag => {
    processedText = processedText.replace(new RegExp(`<${tag}.*?>(.*?)</${tag}>`, 'gs'), '');
  });

  boldContent.forEach(tag => {
    processedText = processedText.replace(new RegExp(`<${tag}.*?>(.*?)</${tag}>`, 'gs'), `\n**${tag}**: $1\n`);
  });

  foldContent.forEach(tag => {
    const new_tag = foldContentMapping[tag] || tag;
    processedText = processedText.replace(new RegExp(`<${tag}.*?>(.*?)</${tag}>`, 'gs'), (match, content) => `<details><summary>\n${new_tag}\n</summary>\n\n${content}\n</details>`);
  });

  processedText = removeUnpairedBackslashXmlTags(processedText).trim()

  const removeString = ["EMPTY MESSAGE", "EMPTY_MESSAGE"]
  removeString.forEach(string => {
    processedText = remove_string(processedText, string)
  })

  return processedText
}