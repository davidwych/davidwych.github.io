---
title: "AlphaFold Has a Data Problem, It's Just Not The One We're Talking About"
mathjax: false
layout: post
---

There's a lot of hubbub lately over [AlphaFold (and other Machine Learning protein structure prediction methods) running out of data](https://www.nature.com/articles/d41586-025-00868-9?utm_campaign=9697067-2025%20Announcements&utm_content=328696841&utm_medium=social&utm_source=linkedin&hss_channel=lcp-10549601). We've exhausted the publicly available resources for protein structure data, so pharmaceutical companies are pooling up their vast collection of private data to get a leg up.

Some have argued that these pharmaceutical companies should open-source their troves of data for the public benefit, and I agree. This would be a good and non-zero-sum thing for them to do—they should have done it already.

But, unfortunately, I suspect that this data is not going to make that much of a difference. AlphaFold *does* have a data problem, but it's not that we need more of what we already have. We need something altogether *different*.

<!--more-->

---
## You get out what you put in

I'm going to assume that you, dear reader, have some cursory understanding of how machine learning (particularly, deep learning) works. You take an enormous inscrutable tangle of digital "neurons", feed a gigantic amount of data through it, and somehow this incomprehensible mass of linear algebra learns the underlying structure in the data well enough to predict new data (of the same kind) very accurately. Feed one of these things all the text on the internet, fine-tune it to be nice and obsequious, and you've got yourself a chatbot that's so good some people sincerely wonder whether or not it's conscious. If only this were profitable.

Now, consider a thought experiment: 

>Rather than training on the entirety of the text available on the internet, imagine that nearly all (say, 90%) of the training data for our current crop of state-of-the-art LLMs was poetry—not beat-nick or avant-garde prose poetry either, *metered verse poetry*. Most of this poetry is written in strict meter, some smaller fraction of it is written in looser meter, but nearly all of the training data is just metered verse poetry.
>
>Let's say that some smaller portion (say 5-10%) of the training data is not poetry, but is still very structured, careful, non-colloquial writing (think instruction manuals, or recipes).
>
>Now, finally, imagine that before the text is fed into the training process, some small but non-negligible fraction of the words in the text (say 5%) were corrupted—swapped out with other words from a dictionary chosen at random.

(*Remember, machine learning models like this only learn from the data they see, and the patterns they uncover—the structure in that data—is only useful for predicting new data that looks like what they've seen.*)

Imagine that you wanted to use one of the LLMs trained above to create a chatbot, like ChatGPT, that can talk naturally and demonstrates some level of understanding across a large range of topics. You want something useful, for generating natural language.

First off, do you think you could even do it? Even though all it's ever seen is poetry and one in twenty words it's seen is just chosen at random, could the LLM still talk naturally and fluently? Do you think you could get the LLM to produce a normal sentence that sounds like you or your friend wrote it?

What kind of sentences, phrases, paragraphs — what domain of the Written Word — do you think this LLM would even be *capable* of producing? How much fine-tuning or additional training do you think you would have to do to get that chatbot to *not* speak in verse? How hard would that be? If you could only fine-tune it on a limited set of text that's *not* poetry, how quickly and effectively do you think it could learn to *forget* the structure of language it's been painstakingly trained to reproduce?

How much about *language or the meanings of words and phrases in general* do you think this LLM would actually understand? Do you think it would contain, though learning from this data, the ability to write an average 8th-grade essay on Napoleon? A coherent run-down of Newton's Second Law? Even a simple, natural-sounding paragraph about tennis?

---

Now, the analogy is not perfect, and I'm intentionally putting a bit of rhetorical top-spin on the ball here, but I think this is more or less the situation we're in with machine learning methods for protein structure prediction, like AlphaFold, right now.

---

## Where the data comes from

To get a sense for why I think this is true, we'll have to talk about the data that AlphaFold is trained on. This data comes from a field of science known as **Structural Biology**. In short, this field is tasked with finding ways to experimentally determine the three-dimensional structure of proteins, nucleic acids, and other molecules that are important to the biological functions of organisms like us. Much of this data is stored in a set of online repositories called the Worldwide Protein Data Bank.

I would argue that the Protein Data Bank is one of the most successful, impactful, and well-administered collaborative scientific projects in history. Through support from a variety of public funding organizations (that are almost surely being gutted as we speak), and buttressed by a vision of open, positive-sum scientific discovery, the human race now maintains a high-quality, free, open-access database of hundreds of thousands of atomic-detail three-dimensional structures of bio-molecules. These structures are the product of the thankless, often grueling work of countless academics, graduate students, post-docs, staff scientists, undergraduates, and private researchers over decades.

### X-ray Crystallography

The overwhelming majority (~82.5%) of this data comes from an experimental technique called **X-ray Crystallography** (XRC). In XRC, concentrated solutions of molecules are coaxed into forming crystals (think of a nice big chunk of sea salt you would find on a bagel, but made out of pure protein). Researchers take these crystals of protein to a facility where they can stick the crystal in the path of a very thin, very high-energy X-ray beam. When you do this, the X-ray beam scatters through the crystal, and if you stick a detector on the other side, you see a pattern of bright spots that changes as you rotate the crystal around. Collect enough of these images, at enough rotation angles, and you can use the information contained in all the bright spots across all the images to reconstruct the three-dimensional structure of the protein in atomic detail.

It's magic, and I explain how it works in more detail [here](https://davidwych.github.io/intro-cryst-1/).

There's one big problem with this method: if you expose the crystal to the X-ray beam for too long, it explodes. "Too long" in this context is on the order of seconds. And I'm being a bit dramatic when I say it "explodes", but [not by much](https://en.wikipedia.org/wiki/Coulomb_explosion). What really happens is the crystal gets irradiated. Electrons get ripped off of atoms, which start to strongly repel each other, and the entire molecule gets damaged to a degree where the structure you're trying to measure in the first place gets eviscerated.

To get around this pesky problem, the crystals are almost always *cryo-cooled*: flooded with a stream of liquid nitrogen, cooled to a temperature of 100 Kelvin (-175 C / -280 F). Cooling the crystal down to such a degree cuts down on the radiation damage, allowing researchers to collect more, higher quality data with the same crystals.

I should say, radiation damage is not the *only* problem with X-ray Crystallography. For one, if you want to use the technique in the first place, you have to get the protein to crystallize. This can be maddeningly difficult to do. If you're studying a protein that usually lives in the cell membrane, you have to strip that membrane away with detergent if you want to get it to crystallize, and that process can destabilize the protein; or the large hydrophobic parts of the protein that cause it to be happy in the cell membrane can make the protein insoluble in water. Proteins can be too floppy or unwieldy to crystallize reliably. Even if you can get crystals to form, they can be extraordinarily delicate or brittle. I once heard a story from a crystallographer that the only way one of their colleagues could get a particular protein to crystallize was if they cut off a small piece of their cat's fur and put that in the solution to serve as a nucleation point. Protein crystallization is a dark art.

But there's another problem that's harder to explain. What we measure in XRC is not the 3D structure of the molecule itself, but the *signature* of that structure in the scattering of the X-ray beam through a crystal. To get a 3D structure out of that mess, we need to *model* the structure, and then compare the expected X-ray scattering of our model with the scattering we observe. If the model gets better, the scattering we predict looks more like the scattering we observe, and we iteratively tweak the model until that agreement is as good as we can reasonably achieve. 

It's a little like trying to make an exact copy of a clay figurine by looking at pictures of the figurine taken from different angles. You keep putting clay in different places, shaving it off in others, molding and smooshing it in certain areas, and holding it up next to the pictures until you think you've gotten as close as you can. Except, in the case of XRC you don't even get to look at images of the clay figurine, you only get to look at the parts of amplitude of that figurine's Fourier Transform that pass through the Ewald sphere at different orientations (don't worry about it — just... it's hard, okay?).

So, how good do our models do? Unfortunately not very well. The measure we use to tell if our models are getting better is called the "R-factor". It's essentially the average error between our predicted spots and the observed spots measured in the diffraction images we collect as we rotate the crystal around in the X-ray beam. We keep tweaking our models and comparing them to experimental data, hoping that the R-factor (the error) goes down. 

The average R-factor between our models and the observed data across the entire PDB is about 25%.

Our models, on average, are 25% off.

This is not very good, and this problem (called the "R-factor Gap") was the focus of a [great paper by James Holton and collaborators from 2014](https://pubmed.ncbi.nlm.nih.gov/25040949/). The "Gap" in "R-factor Gap" refers to the discrepancy between these errors in macro-molecular X-ray crystallography and the errors people tend to see in small-molecule crystallography (where researchers can routinely get R-factors of 5-10% or better). Importantly, they identify that this discrepancy is *not* due to experimental issues or noise—the problem is in the *models we use* in macro-molecular XRC. They identify a few ways we could make the models better: e.g. improving our modeling of the ordered water network and solvent around the protein, and changing the models entirely to capture not just the *structure* of the bio-molecules but also their *dynamics*.

However, it's worth stopping for a second to highlight what we just covered. Something like 80% of our collective knowledge about protein structure comes from a method in which the molecules have to be coaxed into forming a crystal, cooled down to minus 280 degrees Fahrenheit, and stuck in an X-ray beam—and even after we go through the trouble, we don't even measure the structure itself; we just get something we can use to *model* the structure. And most of the time, our models aren't even very great at doing that (at least, not as good as we might hope).

These models are the data that AlphaFold is trained on.

### Cryo-electron Microscopy

Most of the rest of the structures (11%) in the Protein Data Bank were discovered through a different technique called **cryo-Electron Microscopy (cryoEM)**. In cryoEM, you also start with a concentrated solution of protein, but this time, you flood it over a very thin grid (often made of metal with a graphite coating), and dunk that grid in liquid nitrogen, before putting it in the path of an electron beam (you need the liquid nitrogen again because, like X-rays, electron beams irradiate your proteins; but also, if you didn't freeze it, the proteins would just jiggle around all over the place and you couldn't get a good image). As you scan the electron beam over the grid, you can collect images of all the proteins dotted across the grid. These images are two-dimensional projections of the protein in different orientations. Using all these projections, and a bunch of computer power, you can piece together a picture of what the protein looks like in 3D.

This experimental technique is actually much closer, in principle, to our example with the clay figurine from before. Except you get tens- to hundreds-of-thousands of images and you use a computer to do the clay addition and subtraction and molding for you, as it gathers info from all the images of the figurine at different vantage points.

The major issue with *this* technique is that the images you get out of the electron microscope are *extremely* noisy. Sometimes it's hard to even tell that there's anything in them. In my experience, they tend to look like TV static. But, if you collect enough of them, you can still—through the magic of mathematics and computation—get something useful out.

But, like crystallography, what you get out is not the protein structure. You get our a density, and you have to *fit* or "*refine*" a structural model into that density—like fitting a hand in a glove. We're pretty good at this by now, but there are still errors. There are spots where the density is kind of ambiguous and our models are basically just guesses. There are other spots where the density is clear, but we don't really know what's there, so we just guess, and plop something reasonable in. 

Look at enough of these structural models, with the density superimposed, and you don't walk away with *tremendous* confidence. You might trust them generally, in some vague sense, but if someone asked you to bet your life that any one amino acid in any one cryoEM structure picked at random was modeled with unambiguous high confidence, I don't think any Structural Biologist would take the bet.

## NMR

There is another technique that accounts for the remaining 5% or so of the PDB called Nuclear Magnetic Resonance Spectroscopy. It's very cool, and unlike the other two techniques, you don't have to do it at cryo-temperature, and it doesn't produce a single atomic-structural model of the protein, but an *ensemble* of models that capture the protein's motions in solution. But, as I understand it, it only works for very small proteins, and (to be honest) I don't have a very good understanding of how it works. Something about atomic nuclei jiggling in strong magnetic field pulses...? 

The important thing to know about NMR data is that, unlike the other two methods, it directly produces an *ensemble structural model* of the protein. This is very good. I wish there was more data like this, but unfortunately, due to the restrictions discussed above, we just don't have very much of it compared to the single-strutured, non-directly-measured structural models we get from XRC and CryoEM.

In the grand scheme of this post, I feel alright not talking about NMR in too much detail because it makes up a pretty small fraction of the training data people use for protein structure prediction, but also it's very cool, so hey, keep doing what you're doing NMR people.

---

## So, what's this all about?

I mentioned at the start that I don't think pharmaceutical companies pooling their data to train a proprietary version of AlphaFold is really going to make that much of a difference on top of what we already have. I hope now you can understand why.

Ultimately, what we're interested in is not the structures of the proteins *per se*. We want to *do something* with the structures. We want to understand how different biomolecules work. We want to understand how they fold, how they move, how they interact with other molecules. We want to translate that information into a better, more detailed understanding of disease. We want to be able to design drugs that will bind to biomolecules so we can cure those diseases.

Diseases happen to humans, in human bodies. Human bodies don't have many proteins in crystalline form. Human bodies are at 98.6 degrees Fahrenheit, not minus 280. Proteins in the human body don't exist in one single, static folded structure—they move, they jiggle, they come apart and re-form, they have parts that flop around and parts that stay rigid, they interact with other molecules.

The data we currently have is a marvel of human enterprise, ingenuity, and collaboration. Our understanding of protein structure is something to be immensely proud of. But we are still very far from having a clear picture of the true structure and behavior of proteins *in vivo*. The data we have is not useless, and the people that created AlphaFold have done something for which we should all be tremendously grateful. 

I've actually come around on the question of whether they've really "solved" the protein folding problem. I used to be more cynical on this question—producing caveat after caveat to explain why I found that characterization crude. But, in truth, they basically have solved it. Give AlphaFold a sequence of amino acids, and it will spit out a damn good prediction for how that protein folds. It's not perfect, it needs to be skeptically examined, but it's a wild, almost magical, thing that they've accomplished.

But, if we go back to our LLM trained on poetry, we can get a sense for the worst-case scenario of what we might be dealing with here. Given enough training data, I'm confident that our LLM would produce fantastically good poetry. Every kind of poetry we could possibly dream of could be whipped up on a whim. I even think there's a chance that the one in twenty words we swapped out at random wouldn't make all that much of a difference. I think the algorithm would still learn what it needs to bard like few bards have ever barded.

But I don't think that LLM would do very well at all at producing language of any other kind. I don't think it could write a treatise on Bach's inventions. I don't think it could chat naturally, in normal-sounding prose, out of the box. I think it would take a lot of additional data and fine-tuning to get it to be a general-purpose predictor of natural language, like ChatGPT. It wasn't trained to understand the structure of natural language; it was trained to understand the structure of poetry.

And I think we're in a similar position with respect to protein structure prediction right now. I think we have machine learning models that are extraordinarily good at predicting atomic coordinates from structural models produced by X-ray crystallography. But I'm really not all that sure of how well those models correspond to the true structure and dynamics of proteins in the context of human cells, at human body temperature.

### Why does the cryo-temperature part matter?

There's bountiful, solid, peer-reviewed evidence that things change quite dramatically when you bring the temperature up from cryo- to room-temperature, with respect to everything from the [protein structure](https://pmc.ncbi.nlm.nih.gov/articles/PMC8109201/) [itself](https://www.cell.com/structure/fulltext/S0969-2126(14)00140-3), to the [water network](https://elifesciences.org/articles/7574) around [the protein](https://pubs.acs.org/doi/full/10.1021/jacs.9b06275?casa_token=PiCdj6ycnSsAAAAA%3AxTVzXgA2_B6FV3WhHYF_pATeF4MKe6MSzu8RlPSHyDUrMObCQFvk8AsH6gIBojQcO4EXS-yRerBebgmm) (which affect, maybe even *determine*, the binding of small molecules), to [drug-binding](https://elifesciences.org/articles/84632), to [dynamics](https://elifesciences.org/articles/7574), to interactions with other proteins and biomolecules. There's also evidence that some proteins have [different structure and dynamics in the crystalline form](https://pubs.acs.org/doi/pdf/10.1021/bi00539a001?casa_token=2w32fe0TuxkAAAAA:fEYKSjCi0BOcHi4cBxMQySrfVDkWfQRCH8VOFijX6iElvVKTfBgWi-6TwHSdzAeggUgBSiqLIZtlCCIC) [compared to when they are in solution](https://www.sciencedirect.com/science/article/abs/pii/0022283688901052). CryoEM mitigates this latter concern, to some degree, though there's still a lot of effort required to bring the structures we can get out of cryoEM up to the quality of XRC structures.

To make matters worse, from the Machine Learning side, recent evidence is starting to suggest that [deep learning methods like AlphaFold3 (AF3) appear to be mostly memorizing their training data](https://www.biorxiv.org/content/10.1101/2025.04.07.647682v1). 

For drug-discovery in particular, there are a few other things to fret about here, for AF3 in particular, including a lack of reliable correlation with binding affinity data when predicting ligand-bound structures, and significant challenges modeling the conformational changes that result from ligand binding. I’ve heard the arguments that improvements can be made on the dataset preparation / test-train splitting front, and I think it’s definitely true that spending time on this is better than not, but (a) if anyone is going to do this well, DeepMind would do it, and (b) I’m not convinced it makes that much of a difference, except at the margins. The lack of generalization beyond the training data is evidence to me that these models need to be better regularized (in non-obvious ways) but also that the ML models themselves may not be the problem — they can *clearly* learn the underlying structure in this data, so *it’s probably the data that’s the problem*. They’re training on (mostly) single structured models models of X-ray structural data with R-factors of 25% on average collected at cryogenic temperatures, and in this author's humble opinion **we should probably not expect the probability distribution generating this data (however well approximated) to contain information relevant to predicting room-temperature binding affinities**. Proteins are not single structured; protein and ligands don’t bind in the body at cryo temperature; ligands don’t bind in an exact single pose, at an exact location with an exact single-structured active site profile, etc.

### Also, hey, ... water!

The last issue worth discussing about the structural models these deep neural networks are trained on is that they often have the ordered waters stripped from them before they're fed into training! Water (and particularly ordered waters) are tremendously important, not just to the protein structure itself at every scale, but to ligand binding. Stripping out waters before feeding the structures into machine learning models is almost surely contributing to the challenge of predicting accurate ligand binding affinities . Maybe including the ordered waters will make little difference in improving binding-affinity prediction, considering all the other problems we've been discussing (single-structure modelling paradigm, cryo-temperature, deficienties in X-ray strutural models, etc.), but it certainly couldn't hurt.

---

There are a few rays of hope though! Molecular Dynamics (MD) simualtion seems to hold promise for a few reasons. [My work](https://journals.iucr.org/d/issues/2023/01/00/lp5065/index.html) (and [the work of others](https://pubs.acs.org/doi/full/10.1021/acs.jcim.3c01531?casa_token=WO0cwF2xQvEAAAAA%3AONrgHhfSpdD-N_9i9xOFHEm18z1K0ehQ2sfycuel8l-bkVOhV3nkEaRCIEv-EYXveNh7_C5oknLvwIOx)) has shown that crystalline MD simulation can provide better structures and sturctural insight (at least when compared to room temperature X-ray crystallography data) than standard refinement techniques. [Work from my old lab at UC Irvine](https://pubs.rsc.org/en/content/articlehtml/2021/sc/d1sc02751d) has shown that heating cryo-temperature crystal structures up to room-temperature with MD, can reliably recover the room temperature structure/ensemble! Molecular Dynamics simulation may not even be required--Elastic Network Normal Modes (EN/NM) models are quite a bit cheaper and [tend to do quite well](https://www.nature.com/articles/s41467-023-36734-3) in reproducing protein motions in detail, when compared with the appropriate experimental data. Maybe simple EN/NM models like these, on their own, could provide a good starting point to broaden the data these ML models are trained on.

But at the risk of sounding like a broken record, we need to be thinking more about the fact that almost everything we're training on is **not experimental data**, it's **models** of experimental data. We shoud be training on the *actual experimental data*! There are a variety of ways I could imagine doing this, but a good start would just be to attach information about the density and the difference density as information to each atom during training, and teach the model to predict that as well (in addition to the coordinates)! That way you could have the model produce some kind of idea of what the density looks like around every atom (e.g. does this atom live in well-resolved density, or ambiguous density?). Even still, this would not be ideal, because density and difference density in XRC are *determined by the model* as much as the experimental data. Better would be to have the model predict structure factors and train on getting them right (I'm pretty sure most PDB structures published in the last few decades have experimental structure factor data associated with them). But like the rest of the field of structural biology, if the thing you're using to predict the structure factors is a single structure/multi-conformer model with ordered waters and flat-bulk solvent, you're probably not going to do very well.

There are also new *experimental techniques* that could help us, particularly in the realm of measuring and modeling dynamics. Again, cryoEM has some promise to deliver on here (this is what I currently work on). But there are also other techniques in X-ray crystallography itself that could help us. Most of my graduate work concerned something called the "diffuse scattering" in XRC—this is the part of X-ray scattering that's *not* the bright spots we currently use; it's more cloudy, streaky, and it [contains information about correlated motions of the atoms in the crystal](https://www.nature.com/articles/s41467-020-14933-6). We should be working more on leveraging that! Coming up with new models that can capture that motion, and feeding *those* models into our ML algorithms. There's also time-resolved crystallography, time-resolved electron microscopy and tomography, and of course *room-temperature crystallography* ([which I've worked with and modeled, in my career](https://journals.iucr.org/d/issues/2023/01/00/lp5065/index.html)). Room-temperature crystallography is only going to get easier, and we should be doing (and *funding*) more of it. There's so much more to be done—so much more *basic science* to be done—before we could even begin to hope that our machine learning algorithms could predict what we actually *want* out of structural biology.

---

This is not meant to be a rant, or to inspire a kind of fatalism, but to serve as an entry in the Annals of What Machine Learning Can't Do For Us. It can't collect new experimental data to feed itself. It can't invent, or improve, or expand the use of new experimental techniques. It can't fill in gaps in experimental data that we don't yet know how to fill (especially if we don't even know where the gaps are). It can't magically make up for inadequacies in our models, if those models are all the algorithm ever sees.

*We* need to do those things first and foremost, and then maybe the machines will have something insightful to tell us. Or, we could just do the hard work of understanding things for ourselves. [Sorry... now I actually am ranting, but I already wrote a whole thing on that.](https://davidwych.github.io/AI-Art-Science/)
