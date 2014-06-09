import java.util.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.StringReader;

import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

public class DependencyFeatures {
	
	class TagRel{
		String tagStr;
		String relStr;
		String rel;
	}
	
	  public static void main(String[] args) throws FileNotFoundException {
		 // args=new String[]{"csv/test.xls","result.xls"};
	  
	    if (args.length > 0) {
	    	loadFile(args[0],args[1]);
	    } else {
	     
	    }
	  }
	  
	  private  LexicalizedParser lp;
	  private TreebankLanguagePack tlp;
	  private GrammaticalStructureFactory gsf;
	  
	  

	  public DependencyFeatures(){
		  this.lp=LexicalizedParser.loadModel("edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");
		    this.tlp = new PennTreebankLanguagePack();
		    this.gsf = tlp.grammaticalStructureFactory();
		    
		  
	  }
	  
	  
private List<TypedDependency> parseSent(List<CoreLabel> rawWords){
	
    Tree parse = lp.apply(rawWords);
    GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
    
    return gs.typedDependenciesCCprocessed();
}


private ArrayList<TreeGraphNode> filterRel_tag(List<TypedDependency> tdl,int tagIndex){

	ArrayList<TreeGraphNode> ret=new ArrayList<TreeGraphNode>();
	
//	use the token index+1
	for(Iterator<TypedDependency> it = tdl.iterator();it.hasNext();) {
		TypedDependency curRel=it.next();
		
		if(curRel.dep().index()==tagIndex){
			ret.add(curRel.gov());
		}else if(curRel.gov().index()==tagIndex){
			ret.add(curRel.dep());
		}else{
			it.remove();
		}
	  //beginPosition, endPostion, the character offset
//	     if(curRel.dep().label().beginPosition()!=tagIndex&&curRel.gov().label().endPosition()!=tagIndex){
//	    	 it.remove();
//	     }
	     
	     //GrammaticalStructure.getGovernor(TreeGraphNode t)
	     //GrammaticalStructure.getDependents(TreeGraphNode t)
	}
	return ret;
}


	  public ArrayList<TreeGraphNode> parseSentFileTags(String sentence,int index){

		  ArrayList<TreeGraphNode> ret=new ArrayList<TreeGraphNode>();
		    String[] sent = sentence.split("\\s");
		    List<CoreLabel> rawWords = Sentence.toCoreLabelList(sent);
		    List<TypedDependency> tdl=this.parseSent(rawWords);
//		    System.out.println(tdl);
//		    System.out.println(index);
		    ret.addAll(this.filterRel_tag(tdl, index));	

		    return ret;
	  }
	  
	  

	  
	  public ArrayList<String> getRelWords(String sent,int index){
		  ArrayList<TreeGraphNode> tgnl=this.parseSentFileTags(sent,index);
		  ArrayList<String> ret=new ArrayList<String>();
		  for(TreeGraphNode dl:tgnl){
			 ret.add(dl.nodeString());
		  }
		  return ret;
	  }
	  
	  public static void loadFile(String filename,String output) throws FileNotFoundException{
		  DependencyFeatures df=new DependencyFeatures();
		  Scanner scan=new Scanner(new File(filename));
		  PrintWriter printer=new PrintWriter(new File(output));
		  String aline="";
		  String[] words=null;
		  int index=0;
		  String sent="";
		  HashSet<String> wordDict=new HashSet<String>();
		  while(scan.hasNextLine()){
			  aline=scan.nextLine();
			  words=aline.split("\\t");
			  //System.out.println(aline);
			  index=Integer.parseInt(words[5]);
			  sent=words[12];
			  ArrayList<String> relWords=df.getRelWords(sent,index+1);
			  if(relWords!=null&&relWords.size()>0){
				  wordDict.addAll(relWords);
				  for(String aword:relWords){
					  //System.out.println(aword);
					 // System.out.println(aline+"\t"+aword);
					  printer.println(aline+"\t"+aword);
				  }
			  }else{
				  //System.out.println(aline+"\t"+"UNKNOWN");
				  printer.println(aline+"\t"+"UNKNOWN");
			  }
		  }
		  
		  for(String aword:wordDict){
			  System.out.println(aword);
		  }
		  scan.close();
		  printer.close();
		  
	  }
	 
		  
	  }

