import { basename, join } from "path";
import { promises as fs } from "fs";

export const ImageFromSrc = async ( imageBase64: string, key: number=0, alt: string="Image" ) => {
  return <img src={imageBase64} alt={alt} style={{ width: '100%', height: 'auto' }} />
};

export const ImageFromPath = async ( imagePath: string, key?: number ) => {
    const fileName = basename(imagePath);
    const imageData = await fs.readFile(imagePath);
    const base64Image = Buffer.from(imageData).toString('base64');
    const imageSrc = `data:image/png;base64,${base64Image}`;
    return ImageFromSrc(imageSrc, key, fileName);
};

export const ImageFromPaths = ( imagePaths: string[] ) => {
  return (
    <div>
      {imagePaths.map((imagePath, index) => (
        ImageFromPath(join('public/images', imagePath), index)
      ))}
    </div>
  )
};

export class TokenReplacer {
  private readonly targetSequence: string;
  private readonly replacement: string;
  private buffer: string;

  constructor( targetSequence: string, replacement: string ) {
    this.buffer = '';
    this.targetSequence = targetSequence;
    this.replacement = replacement;
  }

  processToken(token: string) {
    this.buffer += token;
    
    var result = '';
    if (!this.targetSequence.includes(this.buffer)) {
      result = this.buffer;
      this.buffer = '';
    } else if (this.buffer.includes(this.targetSequence)){
      this.buffer = this.buffer.replace(this.targetSequence, this.replacement)
      result = this.buffer;
      this.buffer = '';
    }
    return result
  }
}