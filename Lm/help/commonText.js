var relations;

function getRef()
{
	var text;
	
	text = "<a href='http://www.ncbi.nlm.nih.gov/pubmed/18451794'  target='_blank' >";
	text +=	"L-Measure: a web-accessible tool for the analysis, comparison and search of digital reconstructions of neuronal morphologies.";
	text +="</a>";
	text += "<br>";
	text += "Authors:Scorcioni R, Polavaram S, Ascoli GA.";
	document.write(text);
}

//Define all the relations in the method
function funcRel()
{
	relations = new Array();
	
	//Init array for relations
	for( var i = 0; i < 45; i++)
	{
		relations[i] = new Array();
		for( var j = 0; j < 45; j++)
		{
			relations[i][j] = 0;
		}
	}
	
	//Start of Marking relationships
	inRel(3, 4);
	
	inRel(4, 18);
	inRel(4, 23);
	
	inRel(18, 23);
	
	inRel(5, 19);
	inRel(5, 20);
	
	inRel(19, 20);
	
	inRel(6, 7);
	inRel(6, 8);
	
	inRel(7, 8);
	
	inRel(10, 11);
	
	inRel(12, 10);
	inRel(12, 11);
	inRel(12, 13);
	inRel(12, 14);
	inRel(12, 15);
	inRel(12, 16);
	
	inRel(13, 14);
	inRel(13, 15);
	
	inRel(14, 15);
	
	inRel(16, 17);
	
	inRel(17, 23);
	
	inRel(21, 22);
	
	inRel(24, 25);
	
	inRel(26, 27);
	inRel(26, 28);
	
	inRel(27, 28);
	
	inRel(29, 30);
	inRel(29, 31);
	inRel(29, 32);
	
	inRel(30, 31);
	inRel(30, 32);
	
	inRel(31, 32);
	
	inRel(33, 34);
	inRel(33, 35);
	inRel(33, 36);
	inRel(33, 37);
	inRel(33, 38);
	
	inRel(34, 35);
	inRel(34, 36);
	inRel(34, 37);
	inRel(34, 38);
	
	inRel(35, 36);
	inRel(35, 37);
	inRel(35, 38);
	
	inRel(36, 37);
	inRel(36, 38);
	
	inRel(37, 38);
	
	inRel(39, 40);
	inRel(39, 41);
	
	inRel(40, 41);
	
	inRel(43, 44);
	
	
	
}

//Mark rel
function inRel(a,b)
{
	relations[a-1][b-1] = 1;
	relations[b-1][a-1] = 1;
}

function getRel(func)
{
	func--;
	var text = "";
	
	funcRel();
	
	for(var i = 0; i < 45 ; i++)
	{
		if(relations[func][i] == 1 && i != func && (i+1) == 1)
		{
			text += "<a href = 'Soma_Surface.htm'>Soma_Surface</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 2)
		{
			text += "<a href = 'N_stems.htm'>N_stems</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 3)
		{
			text += "<a href = 'N_bifs.htm'>N_bifs</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 4)
		{
			text += "<a href = 'N_branch.htm'>N_branch</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 5)
		{
			text += "<a href = 'N_tips.htm'>N_tips</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 6)
		{
			text += "<a href = 'Width.htm'>Width</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 7)
		{
			text += "<a href = 'Height.htm'>Height</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 8)
		{
			text += "<a href = 'Depth.htm'>Depth</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 9)
		{
			text += "<a href = 'Type.htm'>Type</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 10)
		{
			text += "<a href = 'Diameter.htm'>Diameter</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 11)
		{
			text += "<a href = 'Diameter_pow.htm'>Diameter_pow</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 12)
		{
			text += "<a href = 'Length.htm'>Length</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 13)
		{
			text += "<a href = 'Surface.htm'>Surface</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 14)
		{
			text += "<a href = 'SectionArea.htm'>SectionArea</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 15)
		{
			text += "<a href = 'Volume.htm'>Volume</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 16)
		{
			text += "<a href = 'EucDistance.htm'>EucDistance</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 17)
		{
			text += "<a href = 'PathDistance.htm'>EucDistance</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 18)
		{
			text += "<a href = 'Branch_Order.htm'>Branch_Order</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 19)
		{
			text += "<a href = 'Terminal_degree.htm'>Terminal_degree</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 20)
		{
			text += "<a href = 'TerminalSegment.htm'>TerminalSegment</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 21)
		{
			text += "<a href = 'Taper_1.htm'>Taper_1</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 22)
		{
			text += "<a href = 'Taper_2.htm'>Taper_2</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 23)
		{
			text += "<a href = 'Branch_pathlength.htm'>Branch_pathlength</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 24)
		{
			text += "<a href = 'Contraction.htm'>Contraction</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 25)
		{
			text += "<a href = 'Fragmentation.htm'>Fragmentation</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 26)
		{
			text += "<a href = 'Daughter_Ratio.htm'>Daughter_Ratio</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 27)
		{
			text += "<a href = 'Parent_Daughter_Ratio.htm'>Parent_Daughter_Ratio</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 28)
		{
			text += "<a href = 'Partition_asymmetry.htm'>Partition_Asymmetry</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 29)
		{
			text += "<a href = 'Rall_Power.htm'>Rall_Power</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 30)
		{
			text += "<a href = 'Pk.htm'>Pk</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 31)
		{
			text += "<a href = 'Pk_classic.htm'>Pk_classic</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 32)
		{
			text += "<a href = 'Pk_2.htm'>Pk2</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 33)
		{
			text += "<a href = 'Bif_ampl_local.htm'>Bif_ampl_local</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 34)
		{
			text += "<a href = 'Bif_ampl_remote.htm'>Bif_ampl_remote</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 35)
		{
			text += "<a href = 'Bif_tilt_local.htm'>Bif_tilt_local</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 36)
		{
			text += "<a href = 'Bif_tilt_remote.htm'>Bif_tilt_remote</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 37)
		{
			text += "<a href = 'Bif_torque_local.htm'>Bif_torque_local</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 38)
		{
			text += "<a href = 'Bif_torque_remote.htm'>Bif_torque_remote</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 39)
		{
			text += "<a href = 'Last_parent_diam.htm'>Last_parent_diam</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 40)
		{
			text += "<a href = 'Diam_threshold.htm'>Diam_threshold</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 41)
		{
			text += "<a href = 'HillmanThreshold.htm'>HillmanThreshold</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 42)
		{
			text += "<a href = 'Hausdorff.htm'>Hausdorff</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 43)
		{
			text += "<a href = 'Helix.htm'>Helix</a> ";
			text += "<br>";
		}
		else if(relations[func][i] == 1 && i != func && (i+1) == 44)
		{
			text += "<a href = 'Fractal_Dim.htm'>Fractal Dim</a> ";
			text += "<br>";
		}
		
	}
	if(text.length == 0)
	{
		//document.write("NONE");
	}
	else
	{
		document.write("<div id='sec-type1' style='position: relative; top:20px; left: -155px'>Related Functions : </div> <br>"+text);
	}
}

function showHidden(id)
{
	
	var divId = document.getElementById(id);

	document.getElementById("win7Issue").style.visibility = "hidden";
	document.getElementById("win7VistaSol").style.visibility = "hidden";
	document.getElementById("win7Win7Sol").style.visibility = "hidden";
	document.getElementById("win7AltSol").style.visibility = "hidden";
	document.getElementById("win7Rat").style.visibility = "hidden";
	document.getElementById("win7Impl").style.visibility = "hidden";
	
	divId.style.visibility = "visible";
	
}