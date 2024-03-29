## 1. Introduction
When we host a big party, we typically have several tasks to accomplish. Besides actually doing the work in the party location, we also have to organize all the work, talk with suppliers for food, drinks, and decoration, and deal with the guest list.

Hosting a big party involves a lot of work. So, it would be nice having many people working on it. But, of course, we still need the figure of the party host to make decisions and manage the other people working. But, with multiple people, it’s possible to divide all the required tasks and do them in parallel.

Hosting a party is an analogy to *how a modern computer CPU works*. The **CPU** is our **party host**. It deals with several requests and messages and divides the processing work among the available cores. The **cores**, in turn, are the **people working at the party**. They listen to the host (CPU) instructions and execute the required tasks.

### With this example, we can already note that cores and CPUs are not synonyms.

Thus, in this tutorial, we’ll study the main differences and similarities between them. Initially, we’ll have a brief historical context of processing units. So, we’ll investigate the concepts of cores and CPU. Finally, we’ll compare them in a systematic summary.

# CPU 
A CPU core is a CPU’s processor. In the old days, every processor had just one core that could focus on one task at a time. Today, CPUs have been two and 18 cores, each of which can work on a different task. As you can see in our CPU Benchmarks Hierarchy, that can have a huge impact on performance. 

A core can work on one task, while another core works a different task, so the more cores a CPU has, the more efficient it is. 

Most processors can use a process called `simultaneous multithreading` or, if it’s an Intel processor, `Hyper-threading` (the two terms mean the same thing) to split a core into virtual cores, which are called threads. 

For example, 
AMD CPUs with four cores use simultaneous multithreading to provide eight threads, and most Intel CPUs with two cores use Hyper-threading to provide four threads.

Some apps take better advantage of multiple threads than others. Lightly-threaded apps, like games, don't benefit from a lot of cores, while most video editing and animation programs can run much faster with extra threads.



# PROCESS 


![image](https://github.com/vijayanandrp/blog/assets/3804538/45d6be94-c40f-4b29-b28d-4b6f83a3c589)


![image](https://github.com/vijayanandrp/blog/assets/3804538/2657b2b2-7e5d-4b2e-819e-120d9feb0874)



# Credits:

1. [https://www.baeldung.com/cs/core-vs-cpu](https://www.baeldung.com/cs/core-vs-cpu)
